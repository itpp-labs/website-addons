import werkzeug

from odoo.addons.website_sale.controllers import main as main_file


class QueryURL(object):
    def __init__(self, path="", **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        is_category = path.startswith("/shop/category/")
        for k, v in list(self.args.items()):
            if is_category and k == "search":
                continue
            kw.setdefault(k, v)
        urls = []
        for k, v in list(kw.items()):
            if v:
                if isinstance(v, list) or isinstance(v, set):
                    urls.append(werkzeug.url_encode([(k, i) for i in v]))
                else:
                    urls.append(werkzeug.url_encode([(k, v)]))
        if urls:
            path += "?" + "&".join(urls)
        return path


main_file.QueryURL = QueryURL
