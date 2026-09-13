# -*- coding: utf-8 -*-
{
    'name': 'Indonesia Clinic Management & SatuSehat FHIR RME Engine (Kemenkes Ready)',
    'version': '18.0.1.0.0',
    'category': 'Healthcare/Medical',
    'summary': 'Klinik Pratama & Apotek RME, SOAP Medical Records, ICD-10 Diagnosis, and SatuSehat HL7 FHIR Bridge with Offline Mock',
    'description': """
Comprehensive Clinic Management & Electronic Medical Record (RME) Suite for Odoo 18 Community Edition.
Compliant with Indonesian Ministry of Health (Kemenkes) SatuSehat HL7 FHIR Standards & UU PDP No. 27/2022.

Core Capabilities:
1. Patient Registry & Triage:
   - 16-Digit NIK & BPJS Kesehatan validation
   - SatuSehat Patient IHIS ID tracking and demographic mapping
2. Electronic Medical Record (RME / Rekam Medis Elektronik):
   - Standard SOAP Documentation (Subjective, Objective, Assessment, Plan)
   - Real-Time Vital Signs logging & Automated BMI computation
   - Indonesian ICD-10 Diagnosis & ICD-9-CM Clinical Procedures
3. Kemenkes SatuSehat FHIR Tri-Mode Gateway:
   - Mode 1: Local Simulation (Offline Mock Engine with zero signup required)
   - Mode 2: Remote Developer Sandbox (api-satusehat-stg.kemkes.go.id)
   - Mode 3: Live Production Gateway (HL7 FHIR Encrypted Sync)
   - Synchronizes FHIR Resources: Encounter, Condition, Observation, MedicationRequest
4. Apotek & Pharmacy Dispensing Integration:
   - Prescription lines with dosage instructions (Signa)
   - Direct integration with Point of Sale (POS) and Dynamic QRIS
5. Zero External Server Overhead - 100% Odoo 18 Community Native - Always Free ($0.00).
""",
    'author': 'Riv Cloud Management',
    'website': 'https://airiv.id',
    'url': 'https://github.com/arivonto/airiv_clinic_indonesia/blob/18.0/static/description/index.html',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': ['base', 'account', 'stock', 'point_of_sale', 'airiv_os_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/icd10_initial_data.xml',
        'views/satusehat_config_views.xml',
        'views/medical_patient_views.xml',
        'views/medical_encounter_views.xml',
        'views/clinic_menu_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
