from extensions import db

class UrlReport(db.Model):
    __tablename__ = 'url_reports'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False, unique=True)
    id_report = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)

    def __init__(self, url, id_report):
        self.url = url
        self.id_report = id_report