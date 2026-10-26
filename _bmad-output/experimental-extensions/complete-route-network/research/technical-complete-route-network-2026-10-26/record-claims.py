import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
project=Path('D:/IBE160-plan-complete-route-network')
claims=[
(1,'unverified','landscape','2026-05-21','Entur documents richer NeTEx than derived GTFS and upload/nightly exports with48h history trim; single publisher.'),
(2,'unverified','patterns','2026-06-08','Point-to-point journey planning filters alternatives; cannot establish complete catalogue from travel suggestions.'),
(3,'verified','patterns','2026-04-27','GTFS and independent Nordic model distinguish service date, ordered repeated occurrences and geometry.'),
(4,'unverified','live-observation','2026-10-26','Live line20 returned799 templates,136 active2026-10-26; selected calls expose dates/IDs, but completeness unverified.'),
(5,'verified','live-observation','2026-10-26','Svipper PDF20 weekday Malmvegen05:16 to Skattora06:09 agrees with independently sourced live Entur sample endpoints/aimed times only.'),
(7,'unverified','patterns','2026-09-23','PrivateCode may hold planner trip number but no shift-to-public crosswalk was established.'),
(9,'unverified','live-observation','2026-10-26','Official UI links for Troms NeTEx and GTFS resolve and HEAD200; no ZIP contents parsed.'),
(13,'unverified','live-observation','2026-10-26','Live TRO original import timestamp2026-10-23 differs from archive generation2026-10-25; body timezone unspecified.'),
(14,'unverified','landscape','2026-05-21','NSR provides separate StopPlace/Quay and current/future/historic version exports; no permanence guarantee inferred.'),
(17,'verified','patterns','2025-11-05','Nordic noon-reference DST rule independently corroborates GTFS need for service-day axis; not proof of all producer encodings.'),
(22,'unverified','versions-compatibility','2026-08-31','Entur lists TRO SIRI SX but blank GTFS-RT alerts; default SIRI identifiers map to static data.'),
(23,'unverified','patterns','2024-12-02','SIRI SX supports broad and dated journey selectors; actual TRO message association not probed.')]
for ref,status,cls,pub,claim in claims:
 subprocess.run([sys.executable,str(project/'_bmad/scripts/memlog.py'),'append','--workspace',str(root),'--type','claim','--text',f'ref=[{ref}] status=unverified class={cls} pub={pub[:7]} — {claim}'],check=True,stdout=subprocess.DEVNULL)
 if status!='unverified':
  subprocess.run([sys.executable,str(project/'_bmad/scripts/memlog.py'),'append','--workspace',str(root),'--type','claim','--text',f'ref=[{ref}] status={status} class={cls} pub={pub[:7]} — Independent confirmation recorded in digests: {claim}'],check=True,stdout=subprocess.DEVNULL)
(root/'claims.json').write_text(json.dumps([{'claim':f'[{ref}] {claim}','class':cls,'pub_date':pub} for ref,status,cls,pub,claim in claims],ensure_ascii=False,indent=2),encoding='utf-8')
print('Appended claims via installed memlog script; wrote staleness input.')
