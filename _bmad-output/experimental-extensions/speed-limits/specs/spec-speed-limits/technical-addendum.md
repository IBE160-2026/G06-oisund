# Teknisk tillegg og kvalifiseringsporter

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

SL-PLAN-1, kun plan. Gjenbruk [grensesnitt](../../interfaces.md) og eksisterende React/TypeScript–FastAPI–PostgreSQL. Ingen ny tjeneste, database eller nettverkskonfigurasjon er vedtatt. [Epics og stories](../../planning/epics.md) er bestillingen for en senere, særskilt autorisert gjennomføring.

## Kontrakter og ansvar

- **RoadSnapshot:** manifestId/revision, kilde-URL/hash/hentetid, original endret-/virkningstid, katalog-/schema-versjon, ordnede lenkeforekomster med geometri/CRS/lengde, noder og tillatte overganger, detalj→overordnet mapping/felt, type105 id/versjon/2021-verdi, dekning/hull. Manglende versjonsfelt skal være null, ikke en oppfunnet NVDB-nettversjon; hash og tidskontekst binder det faktiske uttrekket.
- **PositionEvidence:** én allerede autorisert posisjonskilde, måle-/mottakstid, accuracy, nullable heading/speed, watchGeneration og livssyklus. Speed er valgfri og ubrukt av fast300m-policy. Ingen ekstern forespørsel per fix.
- **RoadMatch:** manifest/profile/contextGeneration, rettet lenkeforekomst, alongRoadIntervalM, kandidater og avvisningsårsaker; currentRoadQualified, forwardPathQualified og passageQualified er uavhengige. Unknown/null er et gyldig resultat, ikke en feil som fylles med nærmeste veg.
- **LimitDisplay:** current{value|null,reason,evidenceTime}, upcoming{value,changeOccurrenceId,distanceIntervalM,displayDistanceM}|null, separat reason, sourceAge og generations. Ved grenseoverlapp er current null og upcoming skjult. Hele mulig intervall må ha samme anvendelige aktuelle verdi.

Backend forbereder bare begrensede offentlige korridorsnapshots. Lokal evaluator/matcher beholder korte RAM-vinduer. UI må aldri beregne ny grense fra etikett, holdeplassrekkefølge eller gammel panelverdi. Adapter validerer ukjent schema/tegnkoding før atomisk publisering. Snapshotfeil endrer ikke private aktiviteter.

## SL-LAB-1: tallfestet forslag for senere syntetiske kontroller

Dette er en testprofil, **ikke en kvalifisert GPS-/driftsprofil**. Tallene gjør stories testbare uten å love fysisk nøyaktighet. Endringer krever ny profil-ID og gjentatt berørt kvalifisering.

| Parameter | Forslag / begrunnelse |
|---|---|
| Første varsel | Helt positivt avstandsintervall, øvre grense≤300m; behold fast300m. |
| Visning / hysterese | Avrund sentralestimat til10m, min10m foran. Allerede aktivt panel kan bestå til øvre grense320m, deretter bortfall; gjenkomst er samme passering uten ny animasjon. |
| Ferskhet / sekvens | Fixalder≤5s, minst3 tidsordnede konsistente fikser over minst2s, ingen innbyrdes gap>5s. Eksakt terskel lik er tillatt; større avvises. Skal undersøkes på målutstyret. |
| Accuracy / retning | Rapporteringsfilter accuracy≤25m er bare avvisningsfilter. Konsistent bevegelsesretning på rette strekk foreslås innen20grader. Stillstand skaper ingen ny retning; bue vurderes mot lokal tangent. Ingen automatisk tillit fra accuracy/heading alene. |
| Passering | Minst3 nye koherente fikser, hele usikkerhetsintervallet minst5m etter grensen og lovlig topologisk overgang. Hopp alene teller ikke. |
| Syntetisk feilmodell | Kontrollene leverer eksplisitte intervaller, inklusive grenseoverlapp. Ikke gjør nettleserens accuracy direkte til en garantert langsveg-grense. Fysisk feilmodell og kandidatseparasjon må kvalifiseres før live. |
| RAM | Høyst30 fikser og30s (første overskredne grense rydder eldste). Høyst128 passeringsnøkler per økt. Tap av privat kontekst rydder alt; kort pause kan bevare bare deduplisering uten koordinater. |
| Offentlig snapshot | Forslag for senere adapter: høyst500 segmenter/100 grenseobjekter,20 requests,3MB per respons/10MB samlet per forberedelse,2 begrensede retries. Stopp synlig ved tak; ingen automatisk helkommunehøsting. Dagens manuelle research45oppslag er en annen, avsluttet prosess. |
| Kildekontroll | Forslag: sjekk før pilotstart; siste vellykkede kontroll≤24t og snapshot≤7d, ellers ukjent. Kjent ugyldighet stopper straks. Dette garanterer ikke fersk fysisk regulering; datoene må revurderes før bruk. Ingen bakgrunnshøsting. |

## Porter som ikke kan erklæres bestått nå

| Port | Konkret lukking / eier i planen |
|---|---|
| G0: byggautorisasjon | Ferdig/testet V1, kvalifisert rutenett-/posisjonsstøtte og ny brukerbestilling. Gjelder alle implementeringsstories. |
| G1: operativt snapshot | Story1.1: oppdatert kildegrunnlag; detalj/felt/sving-/bussrestriksjoner, alternative veger og dekningskanter avklart per støttet del. Uavklart del forblir utilgjengelig. |
| G2: ikonleveranse | Story1.2: offisiell originalfil for30/40/50/60/70, hash, utgiver, EPS/NLOD-kildekjede og attribusjon; teknisk konvertering kontrolleres. Geonorge-SVG brukes bare ved egen klar vilkårskjede. |
| G3: lokal kvalifisering | Stories1.3–1.6: implementerte algoritmer og senere syntetiske AC-er; selvstendig forventningsgrunnlag og ingen bruk av planlagt veg som fasit for faktisk veg. |
| G4: fysisk pilot | Story1.7: kilde-/skiltkontroll, målutstyr og kvalifisert feilmodell; på forhånd signert akseptvindu for tilgjengelighet og varslingsavstand. Rå kjørehistorikk samles ikke automatisk. |

Ingen teknisk dokumentkontroll i denne oppgaven lukker G0–G4. Forberedte stories er ferdige planartefakter; de er ikke klare til ubetinget produksjonsbygging. Både aktuell grense og forvarsel kreves for første samlede leveranse, selv om de bygges i mindre steg.
