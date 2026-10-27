export type Fault = 'normal' | 'unavailable' | 'conflict' | 'lost';
export type Draft = { duty: string; bus: string; source: string };
export type Notice = { text: string; start: string; end: string; sourceTime: string; url: string; lines: string };
export type Receipt = { id: string; revision: number; resource: 'draft' | 'notice'; value: Draft | Notice };
export type Result = { kind: 'saved'; receipt: Receipt } | { kind: 'unavailable' } | { kind: 'conflict'; current: Receipt } | { kind: 'lost'; id: string };
export const activities = [
  { id: 'tur-1', title: 'Linje 100 · Tur A', time: '26.10.2026 23:35–23:55', place: 'Fiktiv terminal → Sentrum' },
  { id: 'pause', title: 'Pause', time: '26.10.2026 23:55–27.10.2026 00:10', place: 'Ukjent' },
  { id: 'tur-2', title: 'Linje 200 · Tur B', time: '27.10.2026 00:10–00:40', place: 'Sentrum → Fiktiv terminal' },
];
export const initialDraft = (): Draft => ({ duty: 'F-42', bus: '', source: 'Simulert delvis tekst-PDF, side 1: vognløp og planlagte tider tolket. Side 2: fysisk buss og sted for pause kunne ikke tolkes. Kildens oppdateringstid er ukjent.' });
export const initialNotice = (): Notice => ({ text: 'Fiktiv omkjøring\nBruk holdeplass B. Delt lenke gjelder begge linjer.', start: '', end: '', sourceTime: '', url: '', lines: '100, 200' });
const copy = <T,>(v: T): T => structuredClone(v);
// Independent, volatile teaching model. No network, storage or private dependencies.
export class DemoAdapter {
  private sequence = 0;
  private receipts = new Map<string, Receipt>();
  private current = new Map<string, Receipt>();
  save(resource: Receipt['resource'], value: Draft | Notice, revision: number, fault: Fault): Result {
    if (fault === 'unavailable') return { kind: 'unavailable' };
    if (fault === 'conflict') {
      const newer = copy(value);
      if ('duty' in newer) newer.duty = 'F-99'; else newer.text = 'Nyere simulert melding fra en annen økt';
      return { kind: 'conflict', current: this.accept(resource, newer) };
    }
    const current = this.current.get(resource);
    if (current && current.revision !== revision) return { kind: 'conflict', current: copy(current) };
    const receipt = this.accept(resource, value);
    return fault === 'lost' ? { kind: 'lost', id: receipt.id } : { kind: 'saved', receipt };
  }
  private accept(resource: Receipt['resource'], value: Draft | Notice): Receipt {
    const receipt: Receipt = { id: `SIM-${++this.sequence}`, resource, revision: (this.current.get(resource)?.revision ?? 0) + 1, value: copy(value) };
    this.receipts.set(receipt.id, receipt); this.current.set(resource, receipt); return copy(receipt);
  }
  lookup(id: string, fail: boolean) { return fail ? undefined : copy(this.receipts.get(id)); }
  reopen(resource: Receipt['resource']) { return copy(this.current.get(resource)); }
}
