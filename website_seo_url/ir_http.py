# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# Copyright 2021 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import SUPERUSER_ID, api, models
from odoo.http import request

import odoo.addons.http_routing.models.ir_http as ir_http_file
from odoo.addons.base.models.ir_http import RequestUID
from odoo.addons.http_routing.models.ir_http import _UNSLUG_RE, slug as slug_super
from odoo.addons.website.models.ir_http import ModelConverter


def slug(value):
    field = getattr(value, "_seo_url_field", None)
    if field and isinstance(value, models.BaseModel) and hasattr(value, field):
        name = value[field]
        if name:
            return name
    return slug_super(value)


ir_http_file.slug = slug


class ModelConverterCustom(ModelConverter):
    def __init__(self, url_map, model=False, domain="[]"):
        super(ModelConverter, self).__init__(url_map, model)
        #   Original:'(?:(\w{1,2}|\w[A-Za-z0-9-_]+?\w)-)?(-?\d+)(?=$|/)')
        self.regex = r"(?:(\w{1,2}|\w[A-Za-z0-9-_]+?))(?=$|/)"

    def to_python(self, value):
        _uid = RequestUID(value=value, converter=self)
        env = api.Environment(request.cr, _uid, request.context)

        record_id = None
        field = getattr(request.registry[self.model], "_seo_url_field", None)
        if field and field in request.registry[self.model]._fields:
            cur_lang = request.env.lang
            langs = [cur_lang] + [
                lang
                for lang, _ in env["res.lang"].sudo().get_installed()
                if lang != cur_lang
            ]
            # Workaround for error in Odoo 13.0
            #
            #   File "/opt/odoo/custom/src/odoo/odoo/tools/misc.py", line 1177, in get_lang
            #     for code in [lang_code, env.context.get('lang'), env.user.company_id.partner_id.lang, langs[0]]:
            #   File "/opt/odoo/custom/src/odoo/odoo/tools/func.py", line 24, in __get__
            #     value = self.fget(obj)
            #   File "/opt/odoo/custom/src/odoo/odoo/api.py", line 522, in user
            #     return self(su=True)['res.users'].browse(self.uid)
            #   File "/opt/odoo/custom/src/odoo/odoo/models.py", line 5072, in browse
            #     ids = tuple(ids)
            # TypeError: 'RequestUID' object is not iterable - - -
            #
            # Fixed in Odoo 14: https://github.com/odoo/odoo/commit/9247c5e8fde001d9bd53ea2c7cf9144326eda6e0
            env_sudo = api.Environment(request.cr, SUPERUSER_ID, request.context)
            for lang in langs:
                res = (
                    env_sudo[self.model]
                    .with_context(lang=lang)
                    .search([(field, "=", value)])
                )
                if res:
                    record_id = res[0].id
                    break

        if record_id:
            return env[self.model].browse(record_id)

        # fallback to original implementation
        self.regex = _UNSLUG_RE.pattern
        return super().to_python(value)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _get_converters(cls):
        res = super(IrHttp, cls)._get_converters()
        res["model"] = ModelConverterCustom
        return res
