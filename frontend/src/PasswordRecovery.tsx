import { useEffect, useRef, useState } from 'react';

export type RecoveryFields = { username: string; code: string; new_password: string; confirmation: string };
const empty = (): RecoveryFields => ({ username: '', code: '', new_password: '', confirmation: '' });
export function PasswordRecovery({ submit, cancel, busy }: { submit: (fields: RecoveryFields) => Promise<void>; cancel: () => void; busy: boolean }) {
  const [fields, setFields] = useState(empty);
  const [message, setMessage] = useState('');
  const [invalid, setInvalid] = useState<keyof RecoveryFields | null>(null);
  const [focusField, setFocusField] = useState<keyof RecoveryFields | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { heading.current?.focus(); }, []);
  useEffect(() => {
    if (focusField && !busy) document.getElementById('recover-' + focusField)?.focus();
  }, [focusField, busy, message]);
  function feedback(field: keyof RecoveryFields | null, text: string, focus: keyof RecoveryFields | null = field) {
    setInvalid(field); setFocusField(focus); setMessage(text);
  }
  async function save(event: React.FormEvent) {
    event.preventDefault();
    for (const key of ['username', 'code', 'new_password', 'confirmation'] as const) {
      const length = Array.from(fields[key]).length;
      const minimum = key === 'new_password' || key === 'confirmation' ? 12 : 1;
      if (length < minimum || length > (key === 'username' ? 100 : 256)) {
        feedback(key, minimum === 12 ? 'Nytt passord må ha 12–256 tegn.' : 'Kontroller feltet.'); return;
      }
    }
    if (fields.new_password !== fields.confirmation) { feedback('confirmation', 'De nye passordene må være like.'); return; }
    const submitted = fields;
    setFields(empty()); setInvalid(null); setFocusField(null); setMessage('Gjenoppretter tilgang …');
    try { await submit(submitted); }
    catch (error: any) {
      feedback(error?.field === 'code' ? 'code' : null, (error instanceof Error ? error.message : 'Resultatet kunne ikke bekreftes.') + ' Alle feltene er tømt. Fyll inn brukernavn, kode og nytt passord på nytt.', 'username');
    }
  }
  return <section aria-label="Glemt passord">
    <h2 ref={heading} tabIndex={-1}>Glemt passord?</h2>
    <p>Kontakt Jonas, som drifter løsningen, for identitetskontroll og en engangskode til den eksisterende kontoen. Ingen kode sendes automatisk på e-post. Hvis Jonas er utilgjengelig, må du vente.</p>
    <p>Alle enheter blir logget ut. Lagret arbeid beholdes. Etterpå må du logge inn med det nye passordet. Bruk 12–256 tegn; mellomrom beholdes.</p>
    <form aria-label="Gjenopprett tilgang" onSubmit={event => void save(event)}>
      {([['username', 'Brukernavn'], ['code', 'Engangskode'], ['new_password', 'Nytt passord'], ['confirmation', 'Gjenta nytt passord']] as const).map(([key, label]) => <div key={key}>
        <label htmlFor={'recover-' + key}>{label}</label>
        <input id={'recover-' + key} name={key} type={key === 'username' ? 'text' : 'password'} autoComplete={key === 'username' ? 'username' : key === 'code' ? 'off' : 'new-password'} autoCapitalize="none" spellCheck={false} required aria-invalid={invalid === key} aria-describedby={invalid === key ? 'recovery-feedback' : undefined} disabled={busy} value={fields[key]} onChange={event => { setFields(previous => ({ ...previous, [key]: event.target.value })); if (invalid === key) { setInvalid(null); setFocusField(null); setMessage(''); } }} />
      </div>)}
      <p id="recovery-feedback" role="status" aria-live="polite">{message}</p>
      <button type="submit" disabled={busy}>Lagre nytt passord og logg ut alle enheter</button>
      <button type="button" disabled={busy} onClick={() => { setFields(empty()); cancel(); }}>Avbryt</button>
    </form>
  </section>;
}
