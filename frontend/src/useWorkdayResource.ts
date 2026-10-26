import { useEffect, useRef, useState } from 'react';
import { recoverOperation } from './recoverOperation';
import { validLifecycle } from './PrivateWorkdayProgress';

export type ResourceProps = {
  id: string; expiresAt: string;
  request: (path: string) => Promise<any>; mutation: (path: string, body: object) => Promise<any>;
  suspended: boolean; expired: () => void; lock: (value: boolean) => void; availability: (value: boolean) => void;
  shorten?: (value: string) => void;
};
type Record = { workday_id: string; revision: number; expires_at: string };
const canonical = (v: any): string => JSON.stringify(v, (_, value) => value && typeof value === 'object' && !Array.isArray(value) ? Object.fromEntries(Object.keys(value).sort().map(key => [key, value[key]])) : value);
export type Operation = { operation_id: string; expected_revision: number; activity_id?: string };

// Private intent and the original uncertain request live only in this mount.
// Guarded request/mutation wrappers also bind responses to the displayed session.
export function useWorkdayResource<T extends Record>(props: ResourceProps, resource: 'selection' | 'start', validFields: (v: any) => boolean, accepted: (v: T, op: Operation) => boolean) {
  const { id, expiresAt, request, mutation, suspended, expired, lock, availability } = props;
  const [saved, setSaved] = useState<T | null>(null), [comparison, setComparison] = useState<T | null>(null);
  const [pending, setPending] = useState<Operation | null>(null), [proposal, setProposal] = useState<Operation | null>(null);
  const [busy, setBusy] = useState(true), [available, setAvailable] = useState(true);
  const [rejected, setRejected] = useState(false);
  const [message, setMessage] = useState('Henter lagret status …');
  const alive = useRef(true), sending = useRef(false), generation = useRef(0), unresolved = useRef(false);
  const path = '/workdays/' + id + '/' + (resource === 'start' ? 'lifecycle' : resource);
  const valid = (v: any, historical = false): v is T => v && v.workday_id === id && Number.isSafeInteger(v.revision) && v.revision >= 0
    && typeof v.expires_at === 'string' && (historical || Date.parse(v.expires_at) <= Date.parse(expiresAt)) && Date.parse(v.expires_at) > Date.now() && validFields(v);
  function adopt(value: T) { setSaved(value); setComparison(null); setPending(null); setProposal(null); setRejected(false); unresolved.current = false; lock(false); }
  async function current() {
    try {
      const value = await request(path);
      if (!valid(value)) throw Error();
      props.shorten?.(value.expires_at);
      if (alive.current) { setAvailable(true); availability(true); }
      return value;
    } catch (error: any) {
      if ([404, 410].includes(error?.status)) {
        await request('/auth/session');
        if (alive.current) { setAvailable(false); availability(false); }
      }
      throw error;
    }
  }
  async function load() {
    if (sending.current || suspended) return;
    const version = ++generation.current; setBusy(true);
    try {
      const value = await current();
      if (!alive.current || version !== generation.current) return;
      if (unresolved.current) { setSaved(value); setMessage('Plantilgangen er kontrollert. Forsøket er fortsatt uavklart; kontroller eller prøv samme forsøk.'); }
      else { adopt(value); setMessage('Lagret status er hentet.'); }
    } catch (error: any) {
      if (alive.current && version === generation.current) {
        if (error?.status === 401) expired();
        else { if (!unresolved.current) setSaved(null); setMessage('Status kan ikke bekreftes. Kontroller plantilgangen igjen.'); }
      }
    } finally { if (alive.current && version === generation.current) setBusy(false); }
  }
  useEffect(() => { alive.current = true; void load(); return () => { alive.current = false; generation.current++; lock(false); }; }, [id]);
  async function send(activityId?: string, lookup = false) {
    if (!saved || sending.current || suspended || comparison || (!pending && resource === 'selection' && !activityId)) return;
    const operation = pending ?? (rejected ? proposal : null) ?? { operation_id: crypto.randomUUID(), expected_revision: saved.revision, ...(activityId ? { activity_id: activityId } : {}) };
    generation.current++; sending.current = true; unresolved.current = true; lock(true);
    setPending(operation); setProposal(operation); setBusy(true); setMessage('Forsøket er uavklart til svaret er kontrollert.');
    let verifying = false;
    try {
      const status = () => request('/workday-' + resource + '-operations/' + operation.operation_id);
      const mutate = () => mutation('/workdays/' + id + '/' + resource, operation);
      const receipt = lookup ? await status() : pending ? await recoverOperation(status, current, mutate) : await mutate();
      if (!alive.current) return;
      if (!receipt || Object.keys(receipt).sort().join() !== 'operation_id,result' || receipt.operation_id !== operation.operation_id || !valid(receipt.result, true) || !accepted(receipt.result, operation)) throw Error();
      verifying = true;
      const latest = await current();
      if (!alive.current) return;
      if (latest.revision < receipt.result.revision || latest.revision === receipt.result.revision && canonical({ ...latest, expires_at: receipt.result.expires_at }) !== canonical(receipt.result)) throw Error();
      if (latest.revision > receipt.result.revision) {
        if (resource === 'start') { adopt(latest); setMessage('Lagret skiftstatus er hentet.'); return; }
        setPending(null); setComparison(latest); setMessage('Forsøket ble lagret. Et nyere aktivitetsvalg finnes; sammenlign og last inn lagret valg.');
      } else { adopt(latest); setMessage(resource === 'start' ? 'Skiftstart er lagret.' : 'Aktivitetsvalget er lagret.'); }
    } catch (error: any) {
      if (!alive.current) return;
      if (error?.status === 401) { expired(); return; }
      if (!verifying && !lookup && error?.status === 429 && error.apiDetail && Object.keys(error.apiDetail).sort().join() === 'code,message'
        && error.apiDetail.code === resource + '_receipt_capacity' && error.apiDetail.message === 'For mange lagringsforsøk. Vent til tidligere planer utløper.') {
        try {
          const latest = await current(); if (!alive.current) return;
          setSaved(latest); setPending(null); setRejected(true);
          setMessage('Forsøket ble avvist: grensen på 2000 lagringsforsøk er nådd. Forslaget er beholdt. Avbryt forslaget eller prøv igjen når tidligere planer utløper.');
        } catch { if (alive.current) setMessage('Forsøket er uavklart. Kontroller eller prøv samme forsøk.'); }
        return;
      }
      if (!verifying && !lookup && error?.status === 409 && ['Skiftet er avsluttet. Planen er skrivebeskyttet.', 'Lagringsforsøket har annet innhold.', 'Aktivitetsvalget er endret. Sammenlign med lagret verdi.', 'Skiftstatusen er endret. Last inn lagret status.'].includes(error.apiDetail)) {
        try {
          const latest = await current(); if (!alive.current) return;
          if (error.apiDetail === 'Skiftet er avsluttet. Planen er skrivebeskyttet.') {
            const lifecycle = resource === 'start' ? latest : await request('/workdays/' + id + '/lifecycle');
            if (!validLifecycle(lifecycle) || lifecycle.workday_id !== id || !['ended', 'aborted'].includes(lifecycle.state) || Date.parse(lifecycle.expires_at) > Date.parse(latest.expires_at)) throw Error();
            if (!alive.current) return;
            if (resource === 'start') { adopt(latest); setMessage('Skiftet er avsluttet. Avvist skiftstart er avbrutt.'); }
            else { setPending(null); setComparison(latest); setMessage('Skiftet er avsluttet. Valgforslaget ble ikke lagret. Sammenlign og last inn lagret aktivitetsvalg.'); }
            return;
          }
          if (latest.revision <= operation.expected_revision) throw Error();
          setPending(null); setComparison(latest); setMessage('Lagret status er endret i et annet vindu. Forslaget er beholdt. Sammenlign og last inn lagret status.');
        } catch { if (alive.current) setMessage('Forsøket er uavklart. Kontroller eller prøv samme forsøk.'); }
      } else {
        if ([404, 410].includes(error?.status)) { try { await current(); } catch { /* Retain uncertain operation and hide denied authority. */ } }
        if (alive.current) setMessage('Forsøket er uavklart. Kontroller eller prøv samme forsøk.');
      }
    } finally { sending.current = false; if (alive.current) setBusy(false); }
  }
  function resolve(value: T, feedback: string) { adopt(value); setMessage(feedback); }
  return { saved, comparison, pending, proposal, rejected, busy, available, message, load, send, resolve };
}
