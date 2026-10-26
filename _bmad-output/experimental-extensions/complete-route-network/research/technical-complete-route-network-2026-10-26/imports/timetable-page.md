# Timetable Data

import TimetableTable from '../../src/runtime/components/open-data/TimetableTable/TimetableTable'
import { Callout } from 'zudoku/components'

This page lists all our timetable data dumps which are updated daily. All data dumps have permanent URL's and come as NeTEx or GTFS datasets. NeTEx is the official format for public transport data in Norway and is the most complete in terms of available data. GTFS is a downstream format with only a limited subset of the total data, but we generate datasets for it anyway since GTFS can be easier to use and has a wider distribution among international public transport solutions. GTFS sets come in "extended" and "basic" versions.

<Callout type="info">
    Please be aware that certain information, important to journey planning, may
    be lacking in the GTFS files. This is, in particular, true for text-based
    information, which is not supported by GTFS.
</Callout>

## Authentication

Category: National journey planning. License: NLOD

## Format specification

### NeTEx and Norwegian profile

NeTEx (Network and Timetable Exchange) is an XML-based format for sharing public transport data. It is a CEN-standard and is slated to become an EU standard for national datasets.

-   [Read about NeTEx](http://netex-cen.eu/) (external)
-   [Nordic NeTEx profile](https://enturas.atlassian.net/wiki/spaces/PUBLIC/pages/728891481/Nordic+NeTEx+Profile) defines all the elements, and when and how to use them.
-   [White papers](http://netex-cen.eu/?page_id=14) (external)
-   [XSD XML Schema](https://github.com/NeTEx-CEN/NeTEx) (external)

### GTFS

-   [Reference](https://gtfs.org/documentation/schedule/reference/) (external)
-   [Best practice and tools](https://gtfs.org/) (external)


## Timetable Data

All timetable datasets are continuously updated. When a data owner uploads new data, both the relevant regional dataset and the national dataset are automatically updated.

<TimetableTable />

<Callout type="info">
**Note**: * GTFS basic does not use extended route types. ** Despite a number of
            counties being merged in 2020 the affected datasets continue to be delivered
            separately.
</Callout>

-   Whenever new data is uploaded by a data owner an update of the relevant dataset _and_ the national dataset is triggered.
-   Excessive downloading of files may lead to your IP being blocked. We expect that most users will have no need for more than one download per 24 hours.
-   Additionally, all datasets are automatically re-validated and re-exported every night where expired data is trimmed away, retaining data for a maximum of 48 hours back in time. The original creation date, and subsequently the date of the most recent change can be found by checking the `created` timestamp in `CompositeFrame`. For example: `created="2019-05-29T12:59:32.202"`.

## Status of NeTEx completeness from providers

All Norwegian PTA's are sending native NeTEx from their planning system. The railway companies and some commercial PTO's are doing the same, while some are still developing this capability. The minor PTO's with only one or two lines are using AddTransit (GTFS) or the Entur-built tool Nplan (NeTEx).

Planning systems in use by Entur customers capable of exporting Nordic NeTEx profile compliant data:

-   Hastus (by Giro)
-   DG BUSS (by DataGrafikk)
-   Optibus \*
-   Nplan (by Entur) \*
-   Trapeze for public transport (by Trapeze)
-   TrainPlan (by SignatureRail)
-   TurnIt

\* in development
