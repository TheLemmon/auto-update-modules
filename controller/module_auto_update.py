import odoo
from odoo import http
import odoo.modules.registry
from odoo.api import Environment


class AutoUpdateModules(http.Controller):

    @http.route('/web/update_changed_modules', type='http', auth="none")
    def auto_update_modules(self, **kwargs):
        databases = http.db_list()
        domain = [('state', '=', 'installed'), ('name', '=', "module_auto_update")]

        for db in databases:
            try:
                registry_db = odoo.modules.registry.Registry(db)
                with registry_db.cursor() as cr:
                    env = Environment(cr, odoo.SUPERUSER_ID, {})

                    # if module_auto_update is installed on the current db, update modules
                    Module = env['ir.module.module']
                    if Module.search(domain):
                        print(db)
                        Module.upgrade_changed_checksum()

            except Exception:
                pass

        return {}
