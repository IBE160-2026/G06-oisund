# O6: avgrenset gatewayvedlikehold 1. november 2026

Jonas har bestilt integrering og deploy av bare den kvalifiserte gatewayrettelsen.
Ingen passordfunksjonalitet, Python/API/gate-/PostgreSQL-/vertsoppdatering inngår.
V1-taggen skal forbli på d367a0e47198aeecc52358258cb6825eecdc8c4a; ingen ny tag/release.

## Kvalifisert grunnlag og nødvendige driftsgrenser

[Gatewaykvalifikasjonen](https://github.com/IBE160-2026/G06-oisund/blob/533313873c49317a958dc9a2407fad32f916d19f/docs/evidence/o6-gateway-candidate-20261101.md)
og [samlet vedlikeholdsplan](https://github.com/IBE160-2026/G06-oisund/blob/841fbbe337860d06456abf21c6cd0e5501ad5ffc/docs/evidence/o6-maintenance-ready-20261101.md)
beholdes med sine faktiske versjonsgrenser. Produktendringen er identisk runtime-FROM
til nginx1.30.6-alpine-slim/indexdede8895648b461178c3bc604f7eed4423efe5220b2c4d839f5eb3d34ac3f8f7.
Tidligere kvalifisert lokalt image3cae8303e4976d3515db8d515e0d41f53c5a51884a8bc444dfb1046187a65c6a
bevares. Nyeste origin/main ved start er5cee9e03d03d2c9c165c7f8fec64aa3e146959ab.

Standarddeployen stopper også API/gate og tunnelen. Ny `GatewayStage` stopper
derfor før aktivering; `GatewaySwitch` aktiverer kun gateway med --no-deps/--no-build/
--pull never. Gammel stage bygger hele pakken som tidligere; eventuelle nye midlertidige
API/gate-builds blir aldri kjørt. Før gatewaybyttet bindes nye releasealiases til
de eksakte aktive API/gate-image-ID-ene. Dette bevarer også riktige appbyte ved en
senere autostart. Ingen app-/DB-migrering eller restart bestilles.

Gatewaymodusen avviser endringer i backend, frontend, gate, Nginx-mal/hovedkonfig
og løst Compose-oppsett utover releasealias. Den krever forventet aktiv SHA og
eksakt kvalifisert gatewayimage. API/gate/DB-container-ID/image/PID/oppstart/restartteller,
tunnelprosess og boot-ID sammenlignes før/etter. Ved feil returneres bare gatewayen
til gammel release før operasjonen avvises. 18 isolerte Linux-driftstester bestod,
inkludert kilde-/DB-grenser, feil image, selektivt bytte og gatewaytilbakevei.

## Gjennomføring

Status ved denne første dokumentcommiten: produksjonen er frisk på d367a0e;
83GB ledig, ingen failed units, tunnelready200, backup-timer aktiv og boot-ID
44c550dc-d3b9-4222-8f6c-e0dcdac1a991. Ny backup/restore, staging, artefaktkontroll,
deploy og eiertest er ennå ikke rapportert gjennomført. Faktiske resultater legges til
etter hvert utført trinn; ingen gammel test brukes som etterkontroll av ny serverrelease.
