# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MedicalEncounter(models.Model):
    _name = 'medical.encounter'
    _description = 'Kunjungan Pasien & Rekam Medis Elektronik (RME)'
    _order = 'encounter_date desc, id desc'

    name = fields.Char(string="No. Registrasi / Kunjungan", required=True, copy=False, default=lambda self: _('New'))
    patient_id = fields.Many2one('medical.patient', string="Pasien", required=True)
    patient_nik = fields.Char(related='patient_id.nik', string="NIK Pasien")
    practitioner_id = fields.Many2one('res.users', string="Dokter Pemeriksa", default=lambda self: self.env.user, required=True)
    encounter_date = fields.Datetime(string="Waktu Kunjungan", default=fields.Datetime.now, required=True)
    company_id = fields.Many2one('res.company', string="Klinik", default=lambda self: self.env.company)

    # 1. Subjective (S)
    chief_complaint = fields.Text(string="Keluhan Utama (Anamnesis)", required=True)
    medical_history = fields.Text(string="Riwayat Penyakit Sekarang & Dahulu")

    # 2. Objective (O) - Vital Signs
    systolic = fields.Integer(string="Tekanan Darah Sistolik (mmHg)", default=120)
    diastolic = fields.Integer(string="Tekanan Darah Diastolik (mmHg)", default=80)
    heart_rate = fields.Integer(string="Denyut Nadi (bpm)", default=75)
    respiratory_rate = fields.Integer(string="Laju Nafas (x/menit)", default=18)
    temperature = fields.Float(string="Suhu Tubuh (°C)", default=36.5)
    weight = fields.Float(string="Berat Badan (kg)", default=60.0)
    height = fields.Float(string="Tinggi Badan (cm)", default=165.0)
    bmi = fields.Float(string="Indeks Massa Tubuh (BMI)", compute="_compute_bmi", store=True)
    physical_exam = fields.Text(string="Pemeriksaan Fisik")

    # 3. Assessment (A) - ICD-10
    icd10_code = fields.Char(string="Kode ICD-10", default="A09", required=True, help="Kode Diagnosis ICD-10 Standar WHO / Kemenkes")
    diagnosis_name = fields.Char(string="Nama Diagnosis Medis", default="Gastroenteritis and colitis of unspecified origin", required=True)
    clinical_status = fields.Selection([
        ('active', 'Aktif'),
        ('recurrence', 'Kambuh'),
        ('remission', 'Remisi'),
        ('resolved', 'Sembuh'),
    ], string="Status Klinis", default='active', required=True)

    # 4. Plan (P) - Medical Treatment & Prescription
    therapy_plan = fields.Text(string="Rencana Tindakan / Edukasi Pasien")
    prescription_notes = fields.Text(string="Resep Obat / Instruksi Apotek")

    # SatuSehat Interoperability Metadata
    satusehat_sync_status = fields.Selection([
        ('not_synced', 'Belum Sinkron'),
        ('synced', 'Tersinkronisasi Kemenkes'),
    ], string="Status SatuSehat", default='not_synced', copy=False)
    
    satusehat_encounter_id = fields.Char(string="FHIR Encounter UUID", copy=False, readonly=True)
    satusehat_condition_id = fields.Char(string="FHIR Condition UUID", copy=False, readonly=True)
    satusehat_response_log = fields.Text(string="Log Respon SatuSehat", copy=False, readonly=True)

    state = fields.Selection([
        ('draft', 'Antrean / Pendaftaran'),
        ('examination', 'Pemeriksaan Dokter (RME)'),
        ('pharmacy', 'Farmasi / Apotek'),
        ('done', 'Selesai'),
    ], string="Status Kunjungan", default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('medical.encounter') or f"ENC-{fields.Date.today().strftime('%Y%m')}-0001"
        return super(MedicalEncounter, self).create(vals_list)

    @api.depends('weight', 'height')
    def _compute_bmi(self):
        for rec in self:
            if rec.height > 0:
                h_m = rec.height / 100.0
                rec.bmi = round(rec.weight / (h_m * h_m), 2)
            else:
                rec.bmi = 0.0

    def action_start_examination(self):
        self.write({'state': 'examination'})

    def action_send_to_pharmacy(self):
        self.write({'state': 'pharmacy'})

    def action_complete_encounter(self):
        self.action_sync_satusehat_fhir()
        self.write({'state': 'done'})

    def action_sync_satusehat_fhir(self):
        for rec in self:
            config = self.env['airiv.satusehat.config'].get_active_config()
            payload = {
                'patient_ihis': rec.patient_id.satusehat_ihis_id or f"P-{rec.patient_id.nik}",
                'practitioner_id': rec.practitioner_id.id,
                'encounter_date': fields.Datetime.to_string(rec.encounter_date),
                'icd10': rec.icd10_code,
                'diagnosis': rec.diagnosis_name,
                'vitals': {
                    'systolic': rec.systolic,
                    'diastolic': rec.diastolic,
                    'heart_rate': rec.heart_rate,
                    'temperature': rec.temperature,
                }
            }
            res = config.sync_fhir_encounter(payload)
            if res.get('status') == 'success':
                rec.write({
                    'satusehat_sync_status': 'synced',
                    'satusehat_encounter_id': res.get('encounter_id'),
                    'satusehat_condition_id': res.get('condition_id'),
                    'satusehat_response_log': f"[{res.get('mode')}] {res.get('message')}\nEncounter UUID: {res.get('encounter_id')}\nCondition UUID: {res.get('condition_id')}"
                })
