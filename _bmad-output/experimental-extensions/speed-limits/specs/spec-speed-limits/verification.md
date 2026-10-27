# Akseptkriterier og senere verifikasjon

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Dette er en verifikasjonsplan, ikke utførte produkttester. Alle AC-er gjelder både økning og reduksjon der det er relevant. Kildedata, algoritmisk korrekthet og fysisk brukbarhet har separate porter; en bestått syntetisk demonstrasjon kvalifiserer ikke GPS eller skiltene i gata.

## Akseptmatrise

| ID / capability | Senere kontrolloppsett | Forventet resultat |
|---|---|---|
| AC-01 / CAP-1 | Entydig rettet veg, kjent verdi 50 og gyldig snapshot; deretter manglende verdi eller foreldet måling. | Først tydelig aktuelt 50-skilt; så ukjent med korrekt årsak uten tidligere tall. |
| AC-02 / CAP-2 | Kvalifisert neste 30-grense: avstandsintervall 310–320, så 290–300, så 230–240 m. Gjenta 50→70. | Ingen først; deretter mindre 30/70-skilt og ca.-avstand som teller ned. Aktuelt skilt endres ikke. Avstand er veglengde. |
| AC-03 / CAP-2 | Ny økt får første kvalifiserte endring sikkert foran, ca.120 m unna. | Varsel vises straks med ca.120 m; ingen avhengighet av at systemet så en tidligere 300m-passering. |
| AC-04 / CAP-2 | Kvalifiserte terskelmålinger 302/298/301/297 m; videre tilbake over frosset hysteresebånd og frem igjen. | Høyst én aktivering i samme passering; panel oppdateres/trekkes tilbake riktig, uten nye blink ved gjenkomst. Ingen falsk passering. |
| AC-05 / CAP-2/3 | To endringer med 80 m avstand; en tredje kildegrense har samme verdi som naboen. | Nærmeste reelle endring vises først; etter underbygget passering kommer neste straks med korrekt restavstand. Identisk verdi gir ingen ekstra endring. Ingen hopping over ukjent mellomrom. |
| AC-06 / CAP-3 | Posisjonsusikkerhet overlapper grensen; deretter støtter flere koherente målinger hele intervallet på ny side. Gjenta hopp som alene lander langt forbi. | Ingen tidlig ny aktuell verdi. Ved overlapp aktuell ukjent og nedtelling skjult. Underbygget passering gir ny aktuell; hopp alene gjør det ikke. |
| AC-07 / CAP-4 | Rundkjøring mellom førposisjon og neste grense: syntetisk rettet veg 140 m til innkjøring + 40 m bue + 70 m etter utkjøring = 250 m. Først ukvalifisert arm, så kvalifisert riktig arm; motsigende målinger peker mot feil arm. | Sikker aktuell verdi kan bestå uten varsel. Med kvalifisert riktig videre veg vises 250 m. Ved feil arm trekkes varselet tilbake; planlagt veg tvinger ikke match. Ikke bruk luftlinjesnarvei over rundkjøringen. |
| AC-08 / CAP-4 | To parallelle veger, deretter koherent fysisk overgang/kandidatseparasjon; separat planskilt 2D-kryss uten topologisk forbindelse. | Ukjent ved uavklart faktisk veg; først sikre overganger kan gi aktuell. Ingen overgang bare fordi linjene krysser på kartet. |
| AC-09 / CAP-4 | Stopp/kø før kryss: ferske konsistente målinger, så manglende oppdateringer og gammel heading. | Avstanden faller ikke på klokke. Sikker aktuell kan bestå med ferskt belegg; ingen ny retning etableres i stopp. Foreldelse skjuler verdier etter profilen. |
| AC-10 / CAP-2/4 | Vist varsel mister støtte ved datahull/ny uavklart avkjøring; alternativt bortfall av GPS, tunnel, Pause/Off og sen callback. | Ved bare fremoversiktstap beholdes sikker aktuell, varsel fjernes med årsak. Ved posisjonstap skjules berørte verdier. Ingen callback eller automatisk synlighetsretur gjenstarter sensing; eksplisitt gjenopptakelse og ny vegkvalifisering kreves. |
| AC-11 / CAP-4/5 | Avvik, byttet trasé/snapshot/aktivitet, kildeutfall, utløpt data og endret adgang. | Opphev gammel forventet veg/varsel. Aktuell kan komme fra kvalifisert faktisk veg uavhengig av planen. Ingen bruk utenfor gyldig snapshot/tilgang; ingen blanding av versjoner eller datoforfalsket friskhet. |
| AC-12 / CAP-1/5 | Hull, motstrid, feltavhengighet eller kjent ukvalifisert variabel/midlertidig regulering; skilt vises dag/natt med tilgjengelig tekst. | Ingen antatt 50/80, ingen statisk verdi presentert som live variabel tilstand. Dokumentert kilde/lisensspor og riktige originale ikoner; ukjent er lesbart. Ingen lyd, synlig kart, egenfart eller fartsalarm. |

AC-04s enkeltverdier forutsetter liten kvalifisert avstandsusikkerhet; legg også til intervall 295–305 m, som **ikke** får aktivere før øvre grense er høyst 300. AC-07 er en eksplisitt syntetisk illustrasjon, ikke målte lengder eller en observert fartsgrenseplassering i Tromsø. K3 er nå R4/70→50 ved node3251245:200m før innkjøring +18,448m bue =218,448m. Dette er kildeberegnet, ikke fysisk målt. R2/265,519m er avvist på grunn av feltretning.

## Senere gjennomføring og beviskrav

1. **Dokument-/datakvalifisering, nå kildeunderbygget med åpne operative porter:** Kontroller K1–K4, frys manifest v1 og et versjonert profilark med numeriske grenser for alder, sekvenslengde/tid, accuracy/vegalternativer, geometrifeil, passeringsmargin og hysterese. Begrunn også maksimal kildealder, RAM-vindu og innhentingstak. Ukjent verdi er ikke en stilltiende standard. Kontroller rettigheter for 30/40/50/60/70 og alle faktisk nødvendige tilleggsskilt.
2. **Etter ferdig/testet V1, kvalifiserte avhengigheter og separat byggbestilling:** Utfør syntetiske kontroller AC-01–12 mot frosset offentlig geometri og eksplisitt konstruerte målinger. Registrer forventet/faktisk current/upcoming/status, nettverksavstand, passeringstilstand og profil-/snapshotversjon. Ikke bruk stoppestedsorden som oracle for vegmatch. Kontroller null avhengighet til egenfartsvisning.
3. **Senere autorisert fysisk pilot:** Kontroller skilt og vegkoblinger ved CP0–CP3/R1–R4, deretter faktisk nettbrett/OS/nettleser, foreground/HTTPS, tillatelser, kø/stopp, avbrudd/gjenopptakelse og dag/nattlesbarhet. Registrer eksakte enhets-/profilversjoner og avvik uten full kjørehistorikk; ingen innsamling utføres i denne oppgaven.
4. **Beslutningsport:** Sammenhold observert varslingsavstand, manglende varsler og feilvisninger med på forhånd fastsatt fysisk akseptvindu rundt 300 m. Et slikt toleransevindu er ikke kvalifisert nå. Ethvert unsupported aktuelt tall/feil-arm-varsel stopper aksept for berørt del. Delvis dekning merkes eksplisitt; fire kryss eller full korridor kan ikke erklæres bestått fra ett delstrekk.

Reversert retning får eget senere manifest og egne grense-/armkontroller. GPS-fart og dynamisk tidsbasert terskel holdes i separat oppfølging, med CAP-semantikken bevart og uten automatisk alarmutvidelse.

Sporing av tidligere kvalifiseringspunkter: QF-1→K1/K2, QF-2→K2 og signs-and-rights, QF-3→K1/K4 og interfaces, QF-4→AC-01–12, QF-5→fysisk pilot og byggport. Ingen av disse erklæres gjennomført av spesifikasjonen.

Senere gjennomføringsansvar er fordelt i [stories1.1–1.7](../../planning/epics.md); [SL-LAB-1](technical-addendum.md) gjør profilgrenser eksplisitte uten å erklære GPS-kvalifisering bestått. Ingen av AC-01–12 er kjørt som produkttest i denne oppgaven.
