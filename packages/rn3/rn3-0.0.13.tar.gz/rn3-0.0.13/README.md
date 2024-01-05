# rn3: Python tools to help manage EEA Reportnet3

This repository contains tools to ineract with Reportnet3.

## Requirements
* Windows or Linux operating system
* Python x64 3.8 - 3.12

## Installation

From PyPI:

`pip install rn3`


## <u>**Use 1**</u>: Generate Microsoft SQL script to create data tables based on a dataset in Reportnet3

```
import rn3

ds = DatasetModel()
ds.from_url(
    dataset_id=20822,
    api_key="ApiKey 0123456-2789-yyyy-xxxx-zzzzz",
    base_url=r"https://sandbox-api.reportnet.europa.eu",
)
sql_cmd = ds.sql_cmd(database_name="EnergyCommunity", schema_name="annex_XXIV")

print(sql_cmd)
```

output:

```
USE [EnergyCommunity]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [annex_XXIV].[PaMs](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](500) NOT NULL,
	[TitleNational] [nvarchar](500) NULL,
	[IsGroup] [int] NOT NULL,
	[ListOfSinglePams] [nvarchar](500) NULL,
	[ShortDescription] [text] NOT NULL,
	[ReportNet3HistoricReleaseId] [int] NOT NULL,
CONSTRAINT [PK_PaMs] PRIMARY KEY CLUSTERED
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [annex_XXIV].[PaMs]  WITH NOCHECK ADD  CONSTRAINT [FK_PaMs_ReportNet3HistoricReleases] FOREIGN KEY([ReportNet3HistoricReleaseId])
REFERENCES [metadata].[ReportNet3HistoricReleases] ([Id])
ON DELETE CASCADE
GO
ALTER TABLE [annex_XXIV].[PaMs] CHECK CONSTRAINT [FK_PaMs_ReportNet3HistoricReleases]
GO

.
.
.

... for all tables in dataset

```

## <u>**Use 2**</u>: Write Code List Tables and Reference Data to database

Export Reference Data to excel

```
import rn3
dsrd = rn3.DatasetReferenceData()
dsrd.from_xlsx(xlsx_filepath="~/Downloads/Reference Dataset - Reference data.xlsx")
dsrd.to_mssql("osprey", "EnergyCommunity", "annex_XXIV")
```

output

```
writing table: [annex_XXIV].[dict_Sector]
writing table: [annex_XXIV].[dict_Objectives]
writing table: [annex_XXIV].[dict_UnionPolicies]
writing table: [annex_XXIV].[dict_Dimensions]
writing table: [annex_XXIV].[dict_Currencies]
```

Export the Codelist to database

```
ds = rn3.DatasetModel()

ds.from_url(
    dataset_id=60425,
    api_key="ApiKey 7fee1baa-f8f9-49bf-a21b-227749c961d5",
    base_url=r"https://api.reportnet.europa.eu",
)
ds.sql_codelist_data("osprey", "EnergyCommunity", "annex_XXIV")
```

output

```
writing table: [annex_XXIV].[dict_IsGroup]
writing table: [annex_XXIV].[dict_GeographicalCoverage]
writing table: [annex_XXIV].[dict_GHGAffected]
writing table: [annex_XXIV].[dict_TypePolicyInstrument]
writing table: [annex_XXIV].[dict_UnionPolicy]
writing table: [annex_XXIV].[dict_PaMRelateAirQuality]
writing table: [annex_XXIV].[dict_StatusImplementation]
writing table: [annex_XXIV].[dict_ProjectionsScenario]
writing table: [annex_XXIV].[dict_partNDC]
writing table: [annex_XXIV].[dict_Type]
writing table: [annex_XXIV].[dict_PolicyImpacting]
```

### Contributor note

Before commit, run pre-commit hook
`pip install pre-commit`
`pre-commit run -a`

Connect to DB using sqlalchmy and odbc

```
from sqlalchemy import create_engine

servername = "osprey"
dbname = "EnergyCommunity"
engine = create_engine('mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
conn = engine.connect()
```
