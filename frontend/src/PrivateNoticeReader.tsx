import { useEffect, useRef, useState } from 'react';
import { NoticeFacts, validNotice, type Notice } from './PrivateNotices';

type Candidate = { notice: Notice; matching_lines: string[]; unmatched_tags: string[]; line_uncertain: boolean; validity: 'known' | 'partial' | 'unknown' };
type Result = { workday_id: string; expires_at: string; server_now: string; available_lines: string[]; available_dates: string[]; unknown_line_count: number; unmatched_notice_count: number; selected_line: string | null; selected_date: string | null; stored_count: number; candidates: Candidate[] };
const keys = (value: any, expected: string) => value && typeof value === 'object' && Object.keys(value).sort().join() === expected;
const strings = (v: any, max: number) => Array.isArray(v) && v.length <= max && v.every(t => typeof t === 'string' && t.trim() === t && t.length > 0 && Array.from(t).length <= 300) && new Set(v).size === v.length;
const sameMembers = (a: string[], b: string[]) => a.length === b.length && a.every(value => b.includes(value));
function valid(v: any, id: string, expiry: string, line: string, date: string): v is Result {
  return keys(v, 'available_dates,available_lines,candidates,expires_at,selected_date,selected_line,server_now,stored_count,unknown_line_count,unmatched_notice_count,workday_id')
    && typeof v.server_now === 'string' && Number.isFinite(Date.parse(v.server_now)) && v.workday_id === id && typeof v.expires_at === 'string' && Number.isFinite(Date.parse(v.expires_at)) && Date.parse(v.expires_at) <= Date.parse(expiry) && Date.parse(v.expires_at) > Date.now()
    && strings(v.available_lines, 200) && strings(v.available_dates, 400) && v.available_dates.every((d: string) => /^\d{4}-\d{2}-\d{2}$/.test(d) && new Date(d).toISOString().slice(0, 10) === d)
    && Number.isSafeInteger(v.unknown_line_count) && v.unknown_line_count >= 0 && v.unknown_line_count <= 200
    && Number.isSafeInteger(v.unmatched_notice_count) && v.unmatched_notice_count >= 0 && v.unmatched_notice_count <= v.stored_count
    && v.selected_line === (line || null) && v.selected_date === (date || null) && (!line || v.available_lines.includes(line)) && (!date || v.available_dates.includes(date))
    && Number.isSafeInteger(v.stored_count) && v.stored_count >= 0
    && Array.isArray(v.candidates) && v.candidates.length <= v.stored_count && new Set(v.candidates.map((c: any) => c?.notice?.id)).size === v.candidates.length
    && v.candidates.every((c: any) => keys(c, 'line_uncertain,matching_lines,notice,unmatched_tags,validity') && validNotice(c.notice, id) && c.notice.status === 'registered' && c.notice.valid_until && Date.parse(c.notice.valid_until) > Date.parse(v.server_now)
      && strings(c.matching_lines, 200) && c.matching_lines.every((l: string) => v.available_lines.includes(l)) && strings(c.unmatched_tags, 50) && typeof c.line_uncertain === 'boolean'
      && sameMembers(c.matching_lines, c.notice.line_scope === 'all' ? v.available_lines : v.available_lines.filter((l: string) => c.notice.line_tags.includes(l)))
      && sameMembers(c.unmatched_tags, c.notice.line_scope === 'all' ? [] : c.notice.line_tags.filter((t: string) => !v.available_lines.includes(t)))
      && (c.notice.line_scope === 'all' || c.matching_lines.length > 0) && (!line || c.matching_lines.includes(line))
      && c.line_uncertain === (c.unmatched_tags.length > 0) && (c.unmatched_tags.length === 0 || v.unmatched_notice_count > 0)
      && c.validity === (c.notice.valid_from && c.notice.valid_until ? 'known' : c.notice.valid_from || c.notice.valid_until ? 'partial' : 'unknown'));
}

export function PrivateNoticeReader(p: { id: string; expiresAt: string; open: boolean; available: boolean; suspended: boolean; request: (path: string) => Promise<any>; expired: () => void; shorten: (value: string) => void; back: () => void; maintenance: () => void }) {
  const [line, setLine] = useState(''), [date, setDate] = useState(''), [retry, setRetry] = useState(0);
  const [result, setResult] = useState<Result | null>(null), [choices, setChoices] = useState<Result | null>(null);
  const [state, setState] = useState<'loading' | 'ready' | 'unavailable'>('loading');
  const [now, setNow] = useState(Date.now()); const serverAnchor = useRef({ instant: Date.now(), elapsed: performance.now() });
  useEffect(() => { const timer = window.setInterval(() => setNow(serverAnchor.current.instant + performance.now() - serverAnchor.current.elapsed), 1000); return () => clearInterval(timer); }, []);
  const generation = useRef(0), title = useRef<HTMLHeadingElement>(null);
  useEffect(() => { if (p.open) title.current?.focus(); }, [p.open]);
  useEffect(() => {
    const version = ++generation.current; setResult(null);
    if (!p.open || !p.available || p.suspended) { setState('unavailable'); return; }
    setState('loading'); let active = true;
    const timer = window.setTimeout(() => { if (active && generation.current === version) { active = false; setResult(null); setState('unavailable'); } }, 15000);
    const query = new URLSearchParams(); if (line) query.set('line', line); if (date) query.set('calendar_date', date);
    const requestedAt = performance.now();
    void p.request('/workdays/' + p.id + '/notice-reader' + (query.size ? '?' + query : '')).then(value => {
      if (!active || generation.current !== version) return;
      if (!valid(value, p.id, p.expiresAt, line, date)) throw Error('Malformed reader result');
      serverAnchor.current = { instant: Date.parse(value.server_now), elapsed: requestedAt }; setNow(serverAnchor.current.instant + performance.now() - requestedAt); setResult(value); setChoices(value); setState('ready'); p.shorten(value.expires_at);
    }).catch(async error => {
      if (!active || generation.current !== version) return;
      setResult(null); setState('unavailable');
      if (error?.status === 401) p.expired();
      if ([404, 410].includes(error?.status)) {
        setChoices(null);
        try { await p.request('/auth/session'); } catch (session: any) { if (active && session?.status === 401) p.expired(); }
        if (active && error?.status === 410 && error.apiDetail === 'Planen er utløpt.') p.shorten(new Date().toISOString());
      }
    }).finally(() => window.clearTimeout(timer));
    return () => { active = false; window.clearTimeout(timer); };
  }, [p.id, p.open, p.available, p.suspended, p.expiresAt, line, date, retry]);
  const trusted = p.open && p.available && !p.suspended && state === 'ready' && result && result.workday_id === p.id && result.selected_line === (line || null) && result.selected_date === (date || null) && Date.parse(result.expires_at) > Date.now() ? result : null;
  return <section className="private-notices" hidden={!p.open} aria-label="Avvik for linjer og datoer">
    <h2 tabIndex={-1} ref={title}>Avvik for linjer og datoer</h2>
    <p>Lagrede manuelle kildeopplysninger sammenlignes med bekreftede linjer og planlagte aktivitetsintervaller. Planlagte intervaller styrer tidsmessig relevans. Utløpte og manuelt avsluttede avvik skjules automatisk; valgt aktivitet endrer ikke utvalget. Ingen garanti for kildedekning, nøyaktig tur eller holdeplass. Kontroller originalkilden.</p>
    <p>Manuell avslutning av et avvik bekrefter ikke at veien er klar.</p>
    <div className="controls"><button disabled={p.suspended} onClick={p.back}>Tilbake til dagen</button><button disabled={p.suspended} onClick={p.maintenance}>Til avviksvedlikehold</button></div>
    <label>Bekreftet linje<select aria-label="Bekreftet linje" disabled={!choices || p.suspended || !p.available} value={line} onChange={e => setLine(e.target.value)}><option value="">Alle bekreftede linjer</option>{choices?.available_lines.map(l => <option key={l} value={l}>{l}</option>)}</select></label>
    <label>Planlagt kalenderdato (Oslo)<select aria-label="Planlagt kalenderdato (Oslo)" disabled={!choices || p.suspended || !p.available} value={date} onChange={e => setDate(e.target.value)}><option value="">Alle planlagte datoer</option>{choices?.available_dates.map(d => <option key={d} value={d}>{d}</option>)}</select></label>
    <button disabled={p.suspended || !p.available} onClick={() => { setResult(null); setState('loading'); setRetry(v => v + 1); }}>Hent avvik på nytt</button>
    <p role="status">{state === 'loading' && p.available && !p.suspended ? 'Henter avvik …' : !trusted ? 'Avviksleseren er utilgjengelig. Prøv igjen eller kontroller originalkilden.' : 'Lagrede avvik er hentet.'}</p>
    {trusted && <>
      {(trusted.unknown_line_count > 0 || trusted.available_lines.length === 0) && <p>Aktiviteter uten oppgitt linje: {trusted.unknown_line_count}. Ingen linje utledes for disse aktivitetene; linjedekningen kan ikke fastslås her.</p>}
      {trusted.unmatched_notice_count > 0 && <p>Lagrede avvik med linjetagger eller ruteoverskrifter uten eksakt samsvar: {trusted.unmatched_notice_count}. Disse kan mangle i utvalget. Ingen linjenumre hentes ut av overskrifter.</p>}
      {trusted.stored_count === 0 ? <p>Ingen avvik er lagret i registeret. Dette bekrefter ikke at linjene er uten avvik.</p> : trusted.candidates.filter(c => Date.parse(c.notice.valid_until!) > now).length === 0 ? <p>Ingen lagrede avvik samsvarer med valget. Dette bekrefter ikke at linjene er uten avvik.</p> : null}
      <ul className="notice-list">{trusted.candidates.filter(c => Date.parse(c.notice.valid_until!) > now).map(c => <li key={c.notice.id}><details><summary><span>{c.notice.title} · {c.notice.status === 'ended_manually' ? 'Avsluttet manuelt' : 'Registrert'}</span><br />Linjer: {c.matching_lines.join(', ') || 'Alle linjer; ingen kjente i planen'}</summary>
        <p>Samsvarende bekreftede linjer: {c.matching_lines.join(', ') || 'Ingen kjente'}</p>
        {c.line_uncertain && <p>Usikkert linjesamsvar. Linjetagger eller ruteoverskrifter uten eksakt samsvar: {c.unmatched_tags.join(', ') || 'Ukjent'}. Ingen linjenumre er hentet ut av overskrifter.</p>}
        {c.validity !== 'known' && <p>{c.validity === 'partial' ? 'Delvis kjent gyldighet' : 'Gyldighet ukjent'}: beholdt som mulig kandidat; tidsmessig samsvar er ikke bekreftet.</p>}
        <NoticeFacts value={c.notice} now={now} />
      </details></li>)}</ul>
    </>}
  </section>;
}
