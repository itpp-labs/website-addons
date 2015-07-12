from openerp import api, models, fields, SUPERUSER_ID, http
from openerp.http import request

from openerp.addons.website_sale.controllers.main import website_sale as controller
from openerp.addons.website_sale.controllers import main as main_file

import werkzeug

class website_sale(controller):

    @http.route(['/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', **post):
        request.context['search_tags'] = search
        if category and search:
            category = None
        return super(website_sale, self).shop(page, category, search, **post)


class Product(models.Model):
    _inherit = 'product.template'

    def _extend_domain(self, domain, context):
        print '_extend_domain', domain, context
        if not (context and context.get('search_tags')):
            return domain
        print 'old domain', domain
        domain = ['|', ('tag_ids', 'ilike', context.get('search_tags'))] + domain
        print 'new domain', domain
        return domain

    def search_count(self, cr, uid, domain, context=None):
        domain = self._extend_domain(domain, context)
        return super(Product, self).search_count(cr, uid, domain, context=context)

    def search(self, cr, uid, domain, context=None, **kwargs):
        domain = self._extend_domain(domain, context)
        return super(Product, self).search(cr, uid, domain, context=context, **kwargs)


class QueryURL(object):
    def __init__(self, path='', **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        is_category = path.startswith('/shop/category/')
        for k,v in self.args.items():
            if is_category and k=='search':
                continue
            kw.setdefault(k,v)
        l = []
        for k,v in kw.items():
            if v:
                if isinstance(v, list) or isinstance(v, set):
                    l.append(werkzeug.url_encode([(k,i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k,v)]))
        if l:
            path += '?' + '&'.join(l)
        return path

main_file.QueryURL = QueryURL
