import datetime

from extensions import db
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy import func

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    
    # Definición de la acción
    action_type = db.Column(db.String(30), nullable=False, index=True) # 'BAN', 'MUTE', 'TIMEOUT'
    target_platform = db.Column(db.String(30), nullable=False, index=True) # 'DISCORD', 'MINECRAFT'
    
    # Actores involucrados
    target_user_id = db.Column(db.String(64), nullable=False, index=True) # Infractor
    
    # Detalles y Evidencias
    reason = db.Column(db.Text, nullable=False)
    # Usamos ARRAY de strings de Postgres para almacenar múltiples URLs de pruebas
    evidence_urls = db.Column(ARRAY(db.Text), nullable=True) 
    
    # Estado de la sanción (Activa / Expirada / Revocada)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Control de tiempos
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True, index=True) # NULL significa permanente
    
    # Datos de Revocación (Unban / Unmute)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=True)
    revoked_by = db.Column(db.String(64), nullable=True)
    revocation_reason = db.Column(db.Text, nullable=True)
    
    def __init__ (self, action_type, target_platform, target_user_id, reason, evidence_urls=[], is_active=False, created_at=None, expires_at=None, revoked_at=None, revoked_by=None, revocation_reason=None):
        self.action_type = action_type
        self.target_platform = target_platform
        self.target_user_id = target_user_id
        self.reason = reason
        self.evidence_urls = evidence_urls
        self.is_active = is_active
        self.created_at = created_at
        self.expires_at = expires_at
        self.revoked_at = revoked_at
        self.revoked_by = revoked_by
        self.revocation_reason = revocation_reason