import os
import sys
from extensions import db
from models.entity.security.UrlReport import UrlReport

def get_by_id(id):
    url = db.session.query(UrlReport).filter(UrlReport.id == id).first()
    return url

def get_by_report_id(id_report):
    url_reports = db.session.query(UrlReport).filter(UrlReport.id_report == id_report).all()
    return url_reports

def add_url_report(url, id_report):
    new_url_report = UrlReport(
        url=url,
        id_report=id_report
    )
    db.session.add(new_url_report)
    db.session.commit()

def delete_url_report(id):
    url_report = get_by_id(id)
    db.session.delete(url_report)
    db.session.commit()