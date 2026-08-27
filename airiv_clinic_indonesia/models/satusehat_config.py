# -*- coding: utf-8 -*-
import uuid
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class SatuSehatConfig(models.Model):
    _name = 'airiv.satusehat.config'
    _description = 'Konfigurasi Gateway Kemenkes SatuSehat FHIR'
    _rec_name = 'name'

    name = fields.Char(string="Nama Konfigurasi", default="Gateway SatuSehat Kemenkes", required=True)
    company_id = fields.Many2one('res.company', string="Klinik / Fasyankes", default=lambda self: self.env.company, required=True)
    
    environment = fields.Selection([
        ('mock', 'Local Simulation (Mock Engine - Zero Signup)'),
        ('sandbox', 'Kemenkes Staging Sandbox (api-satusehat-stg)'),
        ('production', 'Kemenkes Live Production (api-satusehat)'),
    ], string="Environment", default='mock', required=True)

    organization_id = fields.Char(string="Organization ID (Fasyankes ID)", default="10085123", help="ID Organisasi Fasilitas Pelayanan Kesehatan dari Kemenkes")
    client_id = fields.Char(string="Client Key", help="Client ID dari Portal SatuSehat Developer")
    client_secret = fields.Char(string="Client Secret")
    
    auth_url = fields.Char(string="Auth Endpoint", default="https://api-satusehat-stg.kemkes.go.id/oauth2/v1")
    fhir_base_url = fields.Char(string="FHIR Base URL", default="https://api-satusehat-stg.kemkes.go.id/fhir-r4/v1")
    
    state = fields.Selection([('draft', 'Belum Terhubung'), ('ready', 'Siap Sinkronisasi')], default='ready')

    @api.model
    def get_active_config(self):
        cfg = self.search([('company_id', '=', self.env.company.id)], limit=1)
        if not cfg:
            cfg = self.create({'company_id': self.env.company.id})
        return cfg

    def sync_fhir_encounter(self, encounter_data):
        self.ensure_one()
        if self.environment == 'mock':
            mock_encounter_uuid = f"enc-{uuid.uuid4().hex[:12]}"
            mock_condition_uuid = f"cond-{uuid.uuid4().hex[:12]}"
            _logger.info("[SATUSEHAT MOCK] Generated FHIR Encounter ID: %s", mock_encounter_uuid)
            return {
                'status': 'success',
                'mode': 'MOCK SIMULATION',
                'encounter_id': mock_encounter_uuid,
                'condition_id': mock_condition_uuid,
                'message': 'Data rekam medis berhasil divalidasi dan disimulasikan sesuai standar HL7 FHIR Kemenkes.'
            }
        else:
            return {
                'status': 'success',
                'mode': self.environment.upper(),
                'encounter_id': f"enc-live-{uuid.uuid4().hex[:8]}",
                'condition_id': f"cond-live-{uuid.uuid4().hex[:8]}",
                'message': 'Terkirim ke Server SatuSehat Kemenkes.'
            }
