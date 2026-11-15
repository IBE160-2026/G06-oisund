# Arkitekturdokumenter – bussjåførassistenten

Oppdatert 15. november 2026, etter ferdigstilt V1 og publisert V1.0.1.

> **`technology.md` er faglærerens eksterne referanseeksempel om Pytagoras Forlag. Filen er ikke bussassistentens vedtatte arkitektur, teknologistakk, kravliste eller driftsoppskrift.** «Påkrevd», kontoer, miljøvariabler og replikeringstrinn i filen gjelder referanseplattformen. Plassering i denne mappen endrer ikke dokumentets autoritet.

| Dokument | Rolle og leserekkefølge |
|---|---|
| [ARCHITECTURE-SPINE.md](architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md) | Bussassistentens SCOPE-02-arkitekturgrunnlag. Behold de vedtatte grensene; les daterte implementasjons-/driftstillegg for senere levert status. Enkelte avsnitt beskriver et tidligere planleggingspunkt. |
| [Etterfølgende vurdering av teknologireferansen](technology-reference-assessment-2026-11-15.md) | Egen vurdering 15. november av lærerens eksempel mot faktisk V1.0.1 og V1.1.0-kandidat. Inneholder teknologikart, relevansvurdering, kildegrenser og oppfølging. Dette er ikke en opprinnelig designbeslutning eller ny godkjenning. |
| [technology.md](technology.md) | Uendret lærerreferanse, lagt til 12. november i [commit 4d97c76](https://github.com/IBE160-2026/G06-oisund/commit/4d97c76ed7557793ce407c7f6cf6f2c269307475). Beskriver `pytagoras-website-v2`, ikke dette produktet. |
| [V1.0.1-vedlikeholdsrapport](../../../docs/evidence/v1.0.1-maintenance-20261104.md) og [driftsguide](../../../docs/ubuntu-server.md) | Faktisk levert vedlikeholds-/driftsgrunnlag og rapporterte bevisgrenser. Publisert kildeversjon og sist rapportert produksjonsversjon må skilles. |
| [Historisk arkitekturindeks](../archive/pre-scope-02-2026-10-19/README.md) | Planen før SCOPE-02. Tidligere offline-/GPS-/tjenestevalg gjeninnføres ikke ved å lese arkivet. |

For lesere og KI-agenter: identifiser hvilket produkt en kilde beskriver før anbefalinger overføres. Bruk eksisterende eierbeslutninger, den relevante versjonens kode/konfigurasjon og daterte bevis som grunnlag for hva bussassistenten har vedtatt og levert. Et eksternt eksempel gir ikke autorisasjon til stackbytte, nye tjenester, kontoer, hemmeligheter, kodeendring eller deploy.

Dette sporet gjelder **teknologireferansen i `4d97c76`**, og er atskilt fra [PRD-kritikken og PRD-revisjonen](../prds/prd-IBE160-2026-09-21/README.md), som fulgte lærerens separate tilbakemelding i `e01712c`.
