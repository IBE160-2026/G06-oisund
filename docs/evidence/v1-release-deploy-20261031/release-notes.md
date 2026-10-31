Kontrollert prosjekt-V1 for IBE160. Eksakt tagmål: `d367a0e47198aeecc52358258cb6825eecdc8c4a`.

- Godkjent applikasjon med PDF-import, gjennomgang/manuell retting, eksplisitt lagring og planbekreftelse, manuell skiftoppfølging og kildebaserte avvik; React/TypeScript, FastAPI og PostgreSQL.
- Ubuntu-integrasjon med dokumentert deploy/rollback og backup/isolert restore, selvstendig lokal sensoroppskrift med syntetiske data og generert innlogging, samt godkjent repo-refleksjon.
- Sluttkontroll: kilde-/innholdskontroll, 31 vertstester, seks oppskriftsvern, fersk isolert oppstart og faktisk innlogging/import/lagring/gjenåpning. Evidens er knyttet til sine konkrete kildeversjoner; historiske tester er ikke fremstilt som nye kjøringer.

O3–O6 har avgrensede delresultater og forblir åpne som godkjent driftsoppfølging etter V1: øvrig ekstern request-/skrivetiming, uavhengig WAN/IPv6, faktisk OS-DNS-kansellering og bredere OS/supply-chain/sikkerhetsdekning. Langtidsstabilitet og registrert libc6-omstartsbehov følges opp separat. Dette er ikke en uttømmende sikkerhetsgodkjenning.

[Sluttrapport og evidens](https://github.com/IBE160-2026/G06-oisund/blob/v1.0.0/docs/evidence/v1-final-control-20261031.md). Releasen er prosjektets V1; komplett kursinnlevering er en separat handling. Aktiv serverversjon dokumenteres i driftsloggen etter faktisk deploy og etterkontroll.

