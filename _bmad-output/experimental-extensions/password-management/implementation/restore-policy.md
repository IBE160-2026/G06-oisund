# Vedtatt gjenopprettingspolicy

## Eierbeslutning 2026-11-04 — passord etter databasegjenoppretting

Jonas har godtatt anbefalingen («Den høre grei ut.»): Ved faktisk databasegjenoppretting skal alle gjenopprettede appkontoer, i første omgang Jonas og faglærer, velge nytt passord via en ny administrativ engangskode. Dette gjelder ikke vanlig omstart eller oppdatering.

- Hold trafikken stengt under gjenoppretting og kontroll. Ugyldiggjør alle gjenopprettede appøkter og engangskoder, og blokker innlogging med gjenopprettede passord før appen åpnes igjen.
- Jonas utsteder en ny tidsbegrenset engangskode via uavhengig servertilgang, også til egen appkonto. Hver bruker velger selv nytt passord i appen og logger inn på nytt på enhetene sine.
- En utilgjengelig bruker kan vente: kontoen forblir sperret for vanlig innlogging til gjenoppretting er fullført. Andre brukere skal ikke måtte vente. Innløsningsflyten må fortsatt kunne brukes av den sperrede kontoen.
- Bevar konto-ID, eierskap og arbeidsdata som finnes i backupen. Nyere arbeidsdata kan mangle. Ingen separat kopi av gjeldende passordhasher innføres som alternativ autoritet.

**Beslutningen er avklart; mekanismen er ikke implementert eller kvalifisert.** Avgrenset erstatningsrestore, kontosperring og sikker gjenåpning må fortsatt implementeres, testes isolert og gjennomgås. Tidligere syntetisk hashoppgjør beviser ikke den nye policyen. Praktisk identitetskontroll/kodeoverlevering og øvrige eiertester står åpne. Dette godkjenner ikke produksjonsrestore, deploy eller release.

