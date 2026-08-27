# Indonesia Clinic Management & SatuSehat FHIR RME Engine (Kemenkes Ready)

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo: 18.0 Community](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com)
[![Price: Free ($0.00)](https://img.shields.io/badge/Price-%240.00%20(Free)-green.svg)](https://airiv.id)
[![Kemenkes: SatuSehat FHIR](https://img.shields.io/badge/Kemenkes-SatuSehat%20HL7%20FHIR-emerald.svg)](https://airiv.id)

A modern, comprehensive Electronic Medical Record (RME) and Clinic Management suite built specifically for **Odoo 18.0 Community Edition**. Designed for Indonesian *Klinik Pratama*, *Klinik Utama*, dental practices, and independent *Apotek* requiring compliance with the **Ministry of Health (Kemenkes) SatuSehat HL7 FHIR** standards and **UU PDP No. 27/2022**.

---

## Detailed Capabilities

### 1. Patient Master Registry & Triage
* **Identity Verification**: Enforces 16-digit NIK KTP validation and BPJS Kesehatan integration.
* **SatuSehat IHIS ID**: Automatically links and formats patient SatuSehat Health IDs.
* **Demographics & Allergies**: Clinical allergy alerts, blood type grouping, and complete historical encounter indexing.

### 2. Electronic Medical Record (RME / Rekam Medis Elektronik)
* **Standard SOAP Documentation**:
  * **S (Subjective)**: Chief complaints (*Anamnesis*) and medical history.
  * **O (Objective)**: Full vital signs (Systolic/Diastolic, Heart Rate, Respiration, Temperature) and automated **BMI Computation**.
  * **A (Assessment)**: Pre-configured **ICD-10** diagnoses and clinical disease status.
  * **P (Plan)**: Treatment notes, lifestyle education, and pharmacy prescription lines (*Signa*).

### 3. Kemenkes SatuSehat FHIR Tri-Mode Gateway
* **Mode 1: Local Simulation (Offline Mock Engine)**: Test patient triage, SOAP encounters, and FHIR resource creation instantly with **0 external signups** required.
* **Mode 2: Remote Developer Sandbox**: Direct bridge to `api-satusehat-stg.kemkes.go.id` for interoperability audits.
* **Mode 3: Live Production Gateway**: Encrypted HL7 FHIR payload dispatch for accredited medical facilities.

---

## Validated Commercial Benchmark (Tested & Scrutinized)

The complete clinical workflow was verified under live Odoo 18.0 Community conditions:

1. **Patient Registration**: Registered patient `Bambang Sudarsono` with 16-digit NIK `3171012345670002` and verified SatuSehat IHIS ID generation.
2. **SOAP Clinical Encounter**: Processed encounter `ENC-202608-0001` with vital signs (BP 110/70, Temp 38.5°C), automated BMI computation ($68\text{ kg} / 1.7\text{ m}^2 = 23.53\text{ kg/m}^2$), and primary diagnosis **ICD-10 A09** (*Gastroenteritis and colitis of unspecified origin*).
3. **SatuSehat FHIR Dispatch**: Synchronized encounter payload, generating FHIR Encounter UUID and Condition UUID with complete audit response logging.

---

## Installation & Odoo Configuration Guide

1. **Deploy Module**:
   Place `airiv_clinic_indonesia` inside your Odoo `custom_addons` directory.

2. **Activate Module**:
   * Navigate to **Apps > Update Apps List**.
   * Search for `Indonesia Clinic Management & SatuSehat FHIR RME Engine` and click **Activate**.

3. **Configure SatuSehat Mode**:
   * Open **Klinik & RME > Pengaturan SatuSehat**.
   * Select **Local Simulation** for instant offline practice, or enter your Kemenkes Developer credentials for Sandbox/Production.

---

## Module Specifications

| Specification | Details |
| :--- | :--- |
| **Framework Version** | Odoo 18.0 Community Edition (OWL & App Drawer compliant) |
| **License** | GNU Lesser General Public License v3.0 (LGPL-3) |
| **Price** | Free ($0.00) |
| **Dependencies** | `base`, `account`, `stock`, `point_of_sale` |
| **Standards Compliance** | Kemenkes SatuSehat HL7 FHIR R4, ICD-10, UU PDP No. 27/2022 |
| **Server Overhead** | Zero (Native ORM, direct browser & REST streams) |
