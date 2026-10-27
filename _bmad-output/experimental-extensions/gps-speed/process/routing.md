# Kjøringsruting og beslutninger

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

Leste faktiske rot-AGENTS.md, CLAUDE.md og .claude/skills/sesjonslogg/SKILL.md i prosjektet, samt installerte bmad-spec og bmad-create-epics-and-stories. Ingen underordnede AGENTS/CLAUDE-filer ble funnet i worktreet. Loggbruker: Jonas Øisund; eksisterende prosjekt-issues og fartsgrense-issues ble lest, ikke endret.

resolve_config.py og resolve_customization.py ble kjørt med eksplisitt project-root=D:/IBE160-plan-gps-speed før planutdata. Sandbox nektet først uv og nettverk; samme lesekontroller ble deretter gjennomført med godkjent utvidet tilgang. Ingen global safe.directory eller BMAD-konfigurasjon ble endret. Git-kontroller bruker prosessavgrenset safe.directory ved behov.

[workflow-binding.json](workflow-binding.json) registrerer faktiske standardstier og denne kjøringens eksplisitte utdataoverstyring. Ingen renderer får standardenes felles planning-artifacts som skrivemål. Hvert memlog.py-kall bruker eksplisitt GPS-workspace. Personlige, ignorerte konfigurasjoner fra andre worktrees ble ikke kopiert. TOML-kilden manglet person-/språkverdier; YAML og brukerens språk ga Jonas/Norwegian, og dokumenter er norsk i samsvar med oppdraget.

bmad-spec kjøres headless/express med slug gps-speed. Beslutninger, CAP-er og presiseringer ble skrevet via memlog.py før avledning. Egen story-breakdown i headless spec er ikke brukt; den separate epic-workflowen gir epics.md. Ingen stories.yaml er laget.

Epic-arbeidsflyten bruker kort SPEC og companions som autorisert erstatning for en ny PRD/UX/arkitekturprosess. Kravuttrekk, epicvalg, storyutforming og sluttvalidering ble behandlet i rekkefølge. Brukerens eksplisitte «fortsett selvstendig» overstyrer rutine-menystopp; valgene er forslag for senere gjennomgang, ikke påstått eieraksept. Ingen prepend/append/persistent-facts-handlinger var konfigurert, og on_complete var tom.

BMAD-help ble lest som arbeidsflytens sluttsteg sammen med relevant katalog: neste aktivitet er eiergjennomgang av denne pakken. Ingen build/sprint-arbeidsflyt startes; brukerens stoppgrense gjelder.

Sesjonslogg-oppskriftens format og separate loggcommit beholdes. Brukerens eksplisitte områderegel flytter logger og issues til process/jonas-oisund/ her; eksisterende .logs/ og andre utvidelsers issues er urørt. Ny tom lokal loggmappe starter på 999. Autorisasjon til push gjelder kun origin/codex/plan-gps-speed.
