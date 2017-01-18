# -*- coding: utf-8 -*-
import re

from odoo import models, api
from odoo.http import request
from odoo.addons.website.models import website as website_file
from odoo.addons.website.models.website import slug as slug_super
from odoo.addons.website.models.ir_http import ModelConverter, RequestUID


def slug(value):
    field = getattr(value, '_seo_url_field', None)
    if field and isinstance(value, models.BaseModel) and hasattr(value, field):
        name = getattr(value, field)
        if name:
            return name
    return slug_super(value)


website_file.slug = slug


class ModelConverterCustom(ModelConverter):

    def __init__(self, url_map, model=False, domain='[]'):
        super(ModelConverter, self).__init__(url_map, model)
        self.domain = domain
        #   Original:'(?:(\w{1,2}|\w[A-Za-z0-9-_]+?\w)-)?(-?\d+)(?=$|/)')
        self.regex = r'(?:(\w{1,2}|\w[A-Za-z0-9-_]+?))(?=$|/)'

    def to_url(self, value):
        return slug(value)

    def to_python(self, value):
        _uid = RequestUID(value=value, converter=self)
        env = api.Environment(request.cr, _uid, request.context)

        record_id = None
        field = getattr(request.registry[self.model], '_seo_url_field', None)
        if field and field in request.registry[self.model]._fields:
            cur_lang = request.lang
            langs = []
            if request.website:
                langs = [lg[0] for lg in request.website.get_languages() if lg[0] != cur_lang]
            langs = [cur_lang] + langs
            context = (request.context or {}).copy()
            for lang in langs:
                context['lang'] = lang
                res = env[self.model].sudo().search([(field, '=', value)])
                if res:
                    record_id = res[0].id
                    break
        if not record_id:
            # try to handle it as it a usual link
            m = re.search(r'-?(-?\d+?)(?=$|/)', value)
            if m:
                record_id = int(m.group(1))

        if not record_id:
            return None

        if record_id < 0:
            # limited support for negative IDs due to our slug pattern, assume abs() if not found
            if not request.registry[self.model].exists(request.cr, _uid, [record_id]):
                record_id = abs(record_id)

        return env[self.model].browse(record_id)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _get_converters(cls):
        res = super(IrHttp, cls)._get_converters()
        res['model'] = ModelConverterCustom
        return res
