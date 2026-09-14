# Indonesia Clinic Management & SatuSehat FHIR RME Engine

[![Odoo 18](https://img.shields.io/badge/Odoo-18.0-714B67)](https://www.odoo.com/) [![License LGPL-3](https://img.shields.io/badge/license-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0.html) [![AIRIV](https://img.shields.io/badge/AIRIV-Clinical-0F766E)](https://airiv.id)

Clinic and pharmacy operations for Odoo 18: patient registry, clinical encounters, SOAP records, ICD-10 diagnosis support, prescriptions, and SatuSehat FHIR bridge surfaces.

## Core Capabilities & Architecture

- Patient identity, NIK, medical record number, demographics, and contact context.
- Clinical encounter documentation with subjective, objective, assessment, and plan sections.
- ICD-10 diagnosis and prescription workflows with follow-up instructions.
- Organization, practitioner, patient, and encounter mapping surfaces for SatuSehat FHIR readiness.
- Reviewable records and explicit validation before external exchange.

## Feature & Workflow Automation

1. Configure clinic identity, practitioners, service units, pharmacy, and integration profile.
2. Register or find the patient and verify identity data.
3. Document the encounter, SOAP notes, diagnosis, prescription, and follow-up.
4. Review completeness and integration identifiers before exchange.

## Technical Specifications

- Odoo: `18.0.1.0.0`, Community Edition compatible
- License: LGPL-3
- Domain: clinic, pharmacy, RME, SOAP, ICD-10, and SatuSehat FHIR preparation
- Store assets: `static/description/icon.png`, `banner.png`, and fragment-safe `index.html`

## Installation Guidance

Clone branch `18.0` into the Odoo addons path, restart Odoo, update the Apps list, and install the module. Configure clinic identity, practitioners, service units, pharmacy settings, and integration profiles before use.

## Configuration Checklist

- Verify NIK, medical record number, date of birth, and patient contact data.
- Review SOAP, diagnosis, prescription, and follow-up before closing encounters.
- Restrict clinical records to authorized user groups.
- Validate organization, practitioner, patient, and encounter identifiers before FHIR exchange.

## Repository Layout

```text
airiv_clinic_indonesia/
  models/                 Clinical and patient domain models
  views/                  Clinic menus and forms
  security/               Access rules and groups
  data/                   Clinical reference data
  static/description/     Apps Store assets
  __manifest__.py         Odoo metadata
```

## Contact Info

- Author: AIRIV
- Website: https://airiv.id
- GitHub: https://github.com/arivonto
- Repository: https://github.com/arivonto/airiv_clinic_indonesia
- Odoo series: `18.0`

## Quality Gate

The repository includes the standard-library Apps Store audit and GitHub Actions validation for branch `18.0`, covering manifest metadata, required assets, XML-safe description markup, repository hygiene, and module structure.
