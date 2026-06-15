from .view.auth_routes import auth_bp
from .view.skins_routes import skins_bp
from .view.console_routes import console_bp
from .view.user_routes import user_bp
from .view.server_route import server_bp
from .view.security.reports_routes import reports_bp
from .view.security.report_url_view import report_url_bp
from .view.security.domains.banned_domains_view import banned_domains_bp
from .view.security.domains.domain_category_view import domain_category_bp

from .api.images_api import images_api
from .api.servers_api import servers_api
from .api.security.reports_api import reports_api
from .api.security.banned_domains_api import banned_domains_api