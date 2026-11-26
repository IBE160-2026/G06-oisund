# GPS-beregnet egen fart — forslag V1.4.5

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Planleggingspakken er ferdig for gjennomgang; produktet er ikke implementert eller kvalifisert. V1.4.5 er et versjonsforslag. Godkjent V1 må ferdigstilles og testes før bygging, som krever en egen bestilling.

## Les først

1. [Kort spesifikasjon](specs/spec-gps-speed/SPEC.md).
2. [Ett epic og fire stories](planning/epics.md).
3. [Måling, visning og livssyklus](specs/spec-gps-speed/measurement-and-behavior.md).
4. [Senere verifikasjon og Lenovo-kriterier](specs/spec-gps-speed/verification.md).
5. [Avgrenset kildeundersøkelse](research.md), [avhengigheter og kildegrunnlag](dependencies.md).
6. [Dokumentkontroll](planning/validation.md), [åpne punkter](process/jonas-oisund/issues.md).

Anbefaling: bruk nettleserens rapporterte `coords.speed`, kvalifiser før visning og konverter m/s × 3,6 til km/t. Utsett fart beregnet fra posisjonsdifferanser. Ingen ekstra utjevning i første kandidat; avvisning og utløp skal ikke maskeres av et gammelt gjennomsnitt. Vis `Egen fart (GPS)` tydelig adskilt fra `Registrert fartsgrense`. Manglende eller gammel fart er «—», aldri automatisk 0.

## Arbeidsområde

| Felt | Kontrollert verdi |
|---|---|
| Worktree | D:/IBE160-plan-gps-speed |
| Branch | codex/plan-gps-speed |
| Utgangsbranch | codex/plan-speed-limits |
| Eksakt utgangscommit | 5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c |
| Origin | https://github.com/IBE160-2026/G06-oisund.git |
| Dokumentrot | _bmad-output/experimental-extensions/gps-speed/ |

Utgangsworktreet var rent; lokal utgangsbranch og origin hadde samme commit ved live kontroll. Målbranch og målworktree fantes ikke. Worktreet ble opprettet direkte fra denne commiten uten kopi av ucommittet arbeid eller branchbytte i andre arbeidsområder. Fartsgrenseplanen følger dermed med som committet grunnlag. Posisjons- og rutenettplanene er separate, committede referanser; se dependencies.md.

Alle nye dokumenter, prosessminner, kontrollbevis og logger ligger under dokumentroten. [Kjøringsbinding](process/workflow-binding.json) overstyrer bare denne kjøringens BMAD-utdatastier; ingen delt/global konfigurasjon er endret. Sesjonsloggen føres under process/jonas-oisund/ etter brukerens områderegel og committes separat fra planfilene.

## Neste gjennomgang

Les SPEC og story GS-E1-S4 først. Ta stilling til GPS-D1–D4 og produktvalgene P1/P2 i spesifikasjonen: ingen posisjonsreserve, ingen ekstra utjevning, «<1» ved liten positiv fart og separat manuell start/gjenopptakelse for fart. Deretter vurder om foreslåtte enhetskriterier er tilstrekkelige. Publisering godkjenner ikke bygging eller fysisk innsamling. Fast 300 m-forvarsel er uendret.
