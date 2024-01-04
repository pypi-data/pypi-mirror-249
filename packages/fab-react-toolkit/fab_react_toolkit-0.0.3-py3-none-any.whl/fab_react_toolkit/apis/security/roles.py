from flask_appbuilder.security.sqla.models import Role
from flask_appbuilder.models.sqla.interface import SQLAInterface

from ...interfaces import ModelRestApi


class RolesApi(ModelRestApi):
    # Will allow flask-login cookie authorization on the API
    allow_browser_login = True
    datamodel = SQLAInterface(Role)

    # this also effects schema of related models
    page_size = 200
    max_page_size = 200

    resource_name = "roles"
    list_columns = ['name', 'permissions']

