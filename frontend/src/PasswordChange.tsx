import { useEffect, useRef, useState } from 'react';

export type PasswordFields = { current_password: string; new_password: string; confirmation: string };
const empty = (): PasswordFields => ({ current_password: '', new_password: '', confirmation: '' });

export function PasswordChange({ submit, cancel, busy }: { submit: (fields: PasswordFields) => Promise<void>; cancel: () => void; busy: boolean }) {
  const [fields, setFields] = useState(empty);
  const [message, setMessage] = useState('');
  const [invalid, setInvalid] = useState<keyof PasswordFields | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { heading.current?.focus(); }, []);
  function feedback(field: keyof PasswordFields, text: string) {
    setInvalid(field); setMessage(text);
    requestAnimationFrame(() => document.getElementById('change-' + field)?.focus());
  }
  async function save(event: React.FormEvent) {
    event.preventDefault();
    for (const key of ['current_password', 'new_password', 'confirmation'] as const) {
      const length = Array.from(fields[key]).length;
      if (length < (key === 'current_password' ? 1 : 12) || length > 256) {
        feedback(key, key === 'current_password' ? 'Gjeldende passord må ha 1–256 tegn.' : 'Nytt passord må ha 12–256 tegn.'); return;
      }
    }
    if (fields.new_password !== fields.confirmation) { feedback('confirmation', 'De nye passordene må være like.'); return; }
    const submitted = fields;
    setFields(empty()); setInvalid(null); setMessage('Endrer passord …');
    try { await submit(submitted); }
    catch (error: any) {
      if (error?.field === 'current_password') feedback('current_password', error.message);
      else setMessage(error instanceof Error ? error.message : 'Endringen kunne ikke bekreftes.');
    }
  }
  return <section aria-label="Brukerinnstillinger">
    <h2 ref={heading} tabIndex={-1}>Endre passord</h2>
    <p>Alle enheter blir logget ut når du endrer passord. Lagret arbeid beholdes. Du må logge inn på nytt.</p>
    <p>Bruk 12–256 tegn. Mellomrom beholdes.</p>
    <form aria-label="Endre passord" onSubmit={event => void save(event)}>
      {([['current_password', 'Gjeldende passord'], ['new_password', 'Nytt passord'], ['confirmation', 'Gjenta nytt passord']] as const).map(([key, label]) => <div key={key}>
        <label htmlFor={'change-' + key}>{label}</label>
        <input id={'change-' + key} name={key} type="password" autoComplete={key === 'current_password' ? 'current-password' : 'new-password'} required aria-invalid={invalid === key} aria-describedby={invalid === key ? 'password-feedback' : undefined} disabled={busy} value={fields[key]} onChange={event => setFields(previous => ({ ...previous, [key]: event.target.value }))} />
      </div>)}
      <p id="password-feedback" role="status" aria-live="polite">{message}</p>
      <button type="submit" disabled={busy}>Endre passord og logg ut alle enheter</button>
      <button type="button" disabled={busy} onClick={() => { setFields(empty()); cancel(); }}>Avbryt</button>
    </form>
  </section>;
}
