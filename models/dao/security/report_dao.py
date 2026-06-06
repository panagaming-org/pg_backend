from extensions import db
from models.entity.security.Report import Report

def get_by_id(id):
    report = db.session.query(Report).filter(Report.id == id).first()
    return report

def get_paged(page, per_page):
    reports = db.session.query(Report).paginate(page=page, per_page=per_page)
    return reports
    
def add_report(action_type, target_platform, tarjet_user_id, reason, evidence_urls, is_active=False, created_at=None, expires_at=None, revoked_at=None, revoked_by=None, revocation_reason=None):
    new_report = Report(
        action_type=action_type,
        target_platform=target_platform,
        tarjet_user_id=tarjet_user_id,
        reason=reason,
        evidence_urls=evidence_urls,
        is_active=is_active,
        created_at=created_at,
        expires_at=expires_at,
        revoked_at=revoked_at,
        revoked_by=revoked_by,
        revocation_reason=revocation_reason
    )
    db.session.add(new_report)
    db.session.commit()

def update_report(id_report, action_type, target_platform, tarjet_user_id, reason, evidence_urls, is_active, created_at, expires_at, revoked_at, revoked_by, revocation_reason):
    report = get_by_id(id_report)
    
    report.action_type = action_type
    report.target_platform = target_platform
    report.tarjet_user_id = tarjet_user_id
    report.reason = reason
    report.evidence_urls = evidence_urls
    report.is_active = is_active
    report.created_at = created_at
    report.expires_at = expires_at
    report.revoked_at = revoked_at
    report.revoked_by = revoked_by
    report.revocation_reason = revocation_reason
    
    db.session.commit()