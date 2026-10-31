# Avgrenset O3–O6-reproduksjon

Les [rapportens versjon, grenser og observerte feil](../../docs/evidence/operations-o3-o6-20261031.md) først. Ingen produksjonstester, nettbrett, innlogging/MFA eller private data inngår. Ikke bruk disse verktøyene til en generell penetrasjonstest.

`run.py` kjøres fra repoet med Python3.12+, PowerShell7 og allerede tilgjengelig Docker. Den krever de eksplisitte lokale image-referansene fra den dokumenterte kjøringen, binder dem til immutable ID-er og sammenligner kilde før gjenbruk. Mangler image, stopp og bygg en ny kvalifisert lokal kandidat; ikke erstatt driftsimages. Alle feilinjeksjoner skjer i egne UUID-containere, internt nett eller network-none, uten vertsporter og med tmpfs-PostgreSQL. Den genererte hemmeligheten lever bare i eget ignorert tmp-område og slettes i `finally`.

```powershell
python scripts/operations-followup/run.py
# Bare den nye HTTP-serien, i egen tidsstemplet evidensmappe:
python scripts/operations-followup/run.py --only-http
```

Fullkjøringens faste evidensmappe er laget for denne dokumenterte økten. **Velg ny OUT-mappe før en senere fullkjøring**, slik at historiske resultater ikke overskrives. Første fullkjøring og to HTTP-kjøringer er beholdt i rapporten. `http_loss.py` må aldri startes mot eksisterende database; den krever egen markør og tom accounts-tabell. Python-barneprosessen stoppes etter testen. DNS-metoden endrer kun containerens egne monterte resolverinnstillinger; ingen host- eller produksjons-DNS.

O6 ble kjørt lokalt med Trivy0.76.1, offentlig ZIP og verifisert releasechecksum. Første imagekjøring lastet ned offentlig database. Deretter ble skanningene kjørt med `--offline-scan --skip-db-update`. Eksempel, med faktisk kvalifisert lokal image-ID/ref og eget output:

```powershell
trivy image --image-src docker --scanners vuln --skip-version-check --offline-scan --skip-db-update --no-progress --cache-dir tmp/operations-followup/trivy-cache --format json --output tmp/operations-followup/trivy-api.json <lokal-kvalifisert-image>
```

Kun `/var/lib/dpkg/status`, `/etc/os-release` og `/etc/lsb-release` ble lest fra Ubuntu med eksisterende SSH-tilgang. Filene ble bevart som UTF-8/LF i eget lokalt `host-rootfs`; ingen privat konfigurasjon eller diskimage. Lokal Dockerfile var `FROM scratch`, `COPY etc/ /etc/`, `COPY var/lib/dpkg/status /var/lib/dpkg/status`. Trivy skannet dette metadataimaget. Manglende OS-deteksjon er en mislykket kvalifikasjon, aldri et nullfunn. Ingen oppdateringskommando på serveren.

`audit.py` leser Git-blobs lokalt og skriver bare mønster-ID, fil, blob og linjenummer ved treff. Den normaliserer egne Trivy-resultater og komprimerer det store Ubuntu-advisorysettet. Originale råresultathasher, skannerhash, DB-tid og alle normaliserte funn beholdes; de store råfilene og den nedlastede skanneren er disposable. Verktøyet trenger disse lokale filene når det kjøres; de er bevisst ikke i Git. Mønstre er heuristikker, ikke full hemmelighetsgaranti. Review treff før publisering.

`finalize.py` kontrollerer eksisterende Docker-ID-er, status, PID/oppstart/restartteller, mounts og volumer mot første snapshot. Bare den naturlig roterende `State.Health.Log` utelates; status/failing streak beholdes. Den kontrollerer også at produkt/refleksjon/tagmål er uendret og indekserer evidensbyte. Ikke normaliser bort uforklarte endringer for å få grønt resultat.

Ikke kjør generelt Docker prune, stopp andres containere eller slett eksisterende volumer. Metadataimages slettes bare med egne eksakte tagger etter kontroll av image-ID; øvrig opprydding er begrenset til denne kjøringens eget resolved tmp-område. Verktøyene skal oppdateres med nytt grunnlag, ny evidensmappe og ny eksplisitt kildeidentitet ved senere bruk.
