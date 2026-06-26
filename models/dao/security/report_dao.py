from extensions import db
from models.entity.security.Report import Report
import models.dao.security.url_report_dao as url_report_dao

def get_by_id(id):
    report = db.session.query(Report).filter(Report.id == id).first()
    return report

def get_all():
    reports = db.session.query(Report).all()
    return reports

def get_paged(page, per_page):
    reports = db.session.query(Report).paginate(page=page, per_page=per_page)
    return reports
    
def add_report(username, action_type, target_platform, target_user_id, reason, 
               is_active=False, created_at=None, expires_at=None, 
               evidence_urls=None, revoked_at=None, revoked_by=None, revocation_reason=None):
    
    if expires_at == "":
        expires_at = None
        
    if evidence_urls is None:
        evidence_urls = []

    new_report = Report(
        username=username,
        action_type=action_type,
        target_platform=target_platform,
        target_user_id=target_user_id,
        reason=reason,
        is_active=is_active,
        created_at=created_at,
        expires_at=expires_at,
        revoked_at=revoked_at,
        revoked_by=revoked_by,
        revocation_reason=revocation_reason
    )
    db.session.add(new_report)
    db.session.commit() 
    
    if len(evidence_urls) > 0:
        for url in evidence_urls:
            link = url.get('url') if isinstance(url, dict) else url
            if link:
                url_report_dao.add_url_report(link, new_report.id)

def update_report(id_report, username, action_type, target_platform, target_user_id, reason, 
                  is_active=False, expires_at=None, revoked_at=None, 
                  revoked_by=None, revocation_reason=None):
    if expires_at == "":
        expires_at = None

    report = get_by_id(id_report)
    
    if report:
        report.username = username
        report.action_type = action_type
        report.target_platform = target_platform
        report.target_user_id = target_user_id
        report.reason = reason
        report.is_active = is_active
        report.expires_at = expires_at
        report.revoked_at = revoked_at
        report.revoked_by = revoked_by
        report.revocation_reason = revocation_reason
        
        db.session.commit()
    else:
        raise Exception(f"No se encontró el reporte con ID {id_report}")

def delete_report(id_report):
    report = get_by_id(id_report)
    db.session.delete(report)
    db.session.commit()