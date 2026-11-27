import { useEffect, useRef, useState } from 'react';
import { type Evidence, SourceFacts } from './PrivateAutomaticNotices';
import { osloDateTime } from './dayOverview';
import { automaticNoticeStatus, statusLabel, useOperationalNow } from './operationalNotices';
import { observePrivateTime } from './privateClock';

type Manual = { id: string; title: string; summary: string | null; description: string | null;
  line_scope: string; line_tags: string[]; valid_from: string | null; valid_until: string;
  checked_at: string | null; source_note: string | null };
type Page = {
  server_now: string; manual: Manual[]; automatic: { id: string; content: Evidence; observation: string }[];
  feed: 'complete' | 'collecting' | 'partial' | 'unavailable' | 'never-qualified'; old: boolean; next_cursor: string | null;
};

export function PrivateTrafficNotices({ available, request }: {
  available: boolean; request: (path: string) => Promise<Page>;
}) {
  const [expanded, setExpanded] = useState(false);
  return <details onToggle={event => setExpanded(event.currentTarget.open)}>
    <summary>Les trafikkavvik</summary>
    {expanded && available && <TrafficNotices request={request} />}
  </details>;
}

function TrafficNotices({ request }: { request: (path: string) => Promise<Page> }) {
  const [page, setPage] = useState<Page | null>(null);
  const [failed, setFailed] = useState(false);
  const [cursors, setCursors] = useState<(string | null)[]>([null]);
  const cursor = cursors.at(-1);
  const now = useOperationalNow(true);
  const requestRef = useRef(request);
  requestRef.current = request;

  useEffect(() => {
    let active = true, loading = false;
    setPage(null);
    async function load() {
      if (loading) return;
      const requestedAt = performance.now();
      loading = true;
      try {
        const data = await requestRef.current('/operational-notices' + (cursor ? '?cursor=' + encodeURIComponent(cursor) : ''));
        if (!active) return;
        if (!data || !Array.isArray(data.manual) || !Array.isArray(data.automatic)) throw Error();
        observePrivateTime(data.server_now, requestedAt);
        setPage(data);
        setFailed(false);
      } catch {
        if (active) { setFailed(true); setPage(null); }
      } finally {
        loading = false;
      }
    }
    void load();
    const timer = window.setInterval(load, 3000);
    return () => { active = false; window.clearInterval(timer); };
  }, [cursor]);

  const manual = page?.manual.filter(item => Date.parse(item.valid_until) > now) ?? [];
  const automatic = page?.automatic.flatMap(item => {
    const state = automaticNoticeStatus(item.content, now);
    return state ? [{ ...item, state }] : [];
  }) ?? [];
  return <section aria-label="Trafikkavvik">
    {failed ? <p role="status">Trafikkavvik kunne ikke hentes.</p> : !page && <p role="status">Henter trafikkavvik …</p>}
    {page && <>
      {(page.feed !== 'complete' || page.old) && <p role="status">
        {page.feed === 'partial' || page.feed === 'unavailable'
          ? 'Entur-innhentingen mislyktes helt eller delvis. Tilgjengelige meldinger kan være utdaterte.'
          : 'Entur har foreløpig ikke en fersk, komplett oppdatering.'}
      </p>}
      {manual.length === 0 && automatic.length === 0 && <p>Ingen tilgjengelige trafikkavvik i denne visningen.</p>}
      <ul>
        {manual.map(item => <li key={item.id}><details>
          <summary>{item.title} · {item.valid_from && Date.parse(item.valid_from) > now ? 'Kommende' : 'Aktiv'}</summary>
          <p>{item.line_scope === 'all' ? 'Alle linjer' : 'Linjer ' + item.line_tags.join(', ')} · Gyldig til {osloDateTime(item.valid_until)}</p>
          {item.summary && <p>{item.summary}</p>}{item.description && <p>{item.description}</p>}
          <p>{item.source_note ?? 'Manuelt registrert'} · {item.checked_at ? 'Kilde kontrollert ' + osloDateTime(item.checked_at) : 'Kilde ikke kontrollert manuelt'}</p>
        </details></li>)}
        {automatic.map(item => <li key={item.id}><details>
          <summary>{item.content.summary[0]?.text ?? 'Melding fra Entur'} · {statusLabel[item.state]}</summary>
          <p>Entur SIRI-SX · {item.observation === 'seen' ? 'Sett i komplett uttrekk' : 'Siste observasjon uavklart'}</p>
          <SourceFacts value={item.content} />
        </details></li>)}
      </ul>
      {cursors.length > 1 && <button onClick={() => setCursors(cursors.slice(0, -1))}>Forrige side</button>}
      {page.next_cursor && <button onClick={() => setCursors([...cursors, page.next_cursor])}>Neste side</button>}
    </>}
  </section>;
}
