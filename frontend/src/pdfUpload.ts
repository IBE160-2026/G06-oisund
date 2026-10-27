// A native File may be readable by the page but unavailable to iOS's network
// process. Send a bounded memory snapshot instead; never persist these bytes.
export function readPdfBytes(file: File, signal: AbortSignal): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const readError = () => Object.assign(new Error('PDF-filen kunne ikke leses fra enheten.'), { importFailure: 'file-read' });
    if (signal.aborted) { reject(new DOMException('Avbrutt', 'AbortError')); return; }
    if (file.size <= 0 || file.size > 10 * 1024 * 1024) { reject(readError()); return; }
    const reader = new FileReader();
    let settled = false;
    const finish = (bytes?: ArrayBuffer, error?: unknown) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      signal.removeEventListener('abort', cancel);
      reader.onload = reader.onerror = reader.onabort = null;
      if (reader.readyState === FileReader.LOADING) reader.abort();
      if (bytes) resolve(bytes); else reject(error ?? readError());
    };
    const cancel = () => finish(undefined, new DOMException('Avbrutt', 'AbortError'));
    const timer = setTimeout(() => finish(undefined, readError()), 10000);
    signal.addEventListener('abort', cancel, { once: true });
    reader.onload = () => {
      const bytes = reader.result;
      if (!(bytes instanceof ArrayBuffer) || bytes.byteLength !== file.size) { finish(); return; }
      finish(bytes);
    };
    reader.onerror = () => finish();
    reader.onabort = cancel;
    try { reader.readAsArrayBuffer(file); } catch { finish(); }
  });
}

// The picker and visibility events can arrive in either order. Wait only while
// the same session is being restored; cancellation must release bytes promptly.
export function waitForPdfAccess(ready: () => boolean, unchanged: () => boolean, signal: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const accessError = () => Object.assign(new Error('Tilgangen må kontrolleres på nytt.'), { importFailure: 'access' });
    const finish = (error?: unknown) => {
      clearInterval(poll); clearTimeout(deadline);
      signal.removeEventListener('abort', cancel);
      if (error) reject(error); else resolve();
    };
    const cancel = () => finish(new DOMException('Avbrutt', 'AbortError'));
    const check = () => {
      if (signal.aborted) cancel();
      else if (!unchanged()) finish(accessError());
      else if (ready()) finish();
    };
    const poll = setInterval(check, 50);
    const deadline = setTimeout(() => finish(accessError()), 10000);
    signal.addEventListener('abort', cancel, { once: true });
    check();
  });
}

export function pdfUploadError(error: any): string {
  if (error?.importFailure === 'access') return 'Tilgangen til opplastingen kunne ikke bekreftes. Kontroller innloggingen og velg PDF-en på nytt.';
  if (error?.importFailure === 'file-read') return 'PDF-filen kunne ikke leses fra enheten. Last den ned til mobilen og velg filen på nytt.';
  if (error?.importFailure === 'response' || error?.status === 200) return 'Serveren returnerte et svar som ikke kunne brukes. Prøv igjen. PDF-en er ikke lagret.';
  if (error?.status === 422 || error?.status === 415) return 'PDF-en kunne ikke tolkes. Den må være en tekst-PDF med støttet skiftkortoppsett, uten kryptering og med høyst 20 sider. Du kan også opprette manuelt utkast.';
  if (error?.status === 413) return 'PDF-en er for stor. Velg en fil på høyst 10 MiB.';
  if (error?.status === 429) return 'Import er opptatt. Prøv igjen eller opprett manuelt utkast.';
  if (error?.status === 403) return 'Tilgangen til opplastingen ble avvist. Last siden på nytt og kontroller innloggingen.';
  if ([408, 504].includes(error?.status) || error?.name === 'TimeoutError') return 'Opplastingen eller tolkingen tok for lang tid. Prøv igjen når forbindelsen er stabil.';
  if (error?.status >= 500) return 'Tjenesten er midlertidig utilgjengelig. Prøv opplastingen igjen senere.';
  if (error?.name === 'AbortError') return 'Opplastingen ble avbrutt. Velg PDF-en på nytt for å prøve igjen.';
  return 'Opplastingen kunne ikke fullføres. Kontroller forbindelsen og prøv igjen. PDF-en er ikke lagret.';
}
