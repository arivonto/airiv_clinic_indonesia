# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class MedicalPatient(models.Model):
    _name = 'medical.patient'
    _description = 'Rekam Pasien Klinik & SatuSehat'
    _inherits = {'res.partner': 'partner_id'}
    _order = 'name asc'

    partner_id = fields.Many2one('res.partner', string="Kontak Pelanggan/Pasien", required=True, ondelete='cascade')
    patient_number = fields.Char(string="No. Rekam Medis (No. RM)", required=True, copy=False, default=lambda self: _('New'))
    
    nik = fields.Char(string="NIK (16 Digit KTP)", size=16, required=True, index=True)
    bpjs_number = fields.Char(string="No. Kartu BPJS Kesehatan", size=13)
    satusehat_ihis_id = fields.Char(string="SatuSehat IHIS ID", copy=False, help="ID Pasien Terverifikasi dari Platform SatuSehat Kemenkes")
    
    gender = fields.Selection([
        ('male', 'Laki-laki (Male)'),
        ('female', 'Perempuan (Female)'),
    ], string="Jenis Kelamin", required=True, default='male')
    
    birth_date = fields.Date(string="Tanggal Lahir", required=True)
    blood_type = fields.Selection([
        ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')
    ], string="Golongan Darah")
    
    allergy_history = fields.Text(string="Riwayat Alergi Obat / Makanan")
    encounter_ids = fields.One2many('medical.encounter', 'patient_id', string="Riwayat Kunjungan / RME")
    encounter_count = fields.Integer(string="Total Kunjungan", compute="_compute_encounter_count")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_number', _('New')) == _('New'):
                vals['patient_number'] = self.env['ir.sequence'].next_by_code('medical.patient') or f"RM-{fields.Date.today().strftime('%Y%m')}-0001"
            if vals.get('nik') and not vals.get('satusehat_ihis_id'):
                # Generate synthetic mock IHIS ID based on NIK in mock environment
                vals['satusehat_ihis_id'] = f"P-{vals['nik']}"
        return super(MedicalPatient, self).create(vals_list)

    @api.constrains('nik')
    def _check_nik_digits(self):
        for rec in self:
            if rec.nik and (len(rec.nik) != 16 or not rec.nik.isdigit()):
                raise ValidationError(_("NIK Pasien wajib tepat 16 digit angka sesuai KTP / Coretax!"))

    def _compute_encounter_count(self):
        for rec in self:
            rec.encounter_count = len(rec.encounter_ids)
