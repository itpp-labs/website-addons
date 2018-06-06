from odoo import api, models, fields

from odoo.tools import html_escape as escape
import werkzeug


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.one
    def _get_website_file_url(self):
        if self.url:
            url = self.url
        else:
            url = self.env['website'].file_url(self)
        self.website_file_url = url

    @api.one
    def _get_website_file_count(self):
        count = 0
        if self.website_file:
            url = escape(self.website_file_url)
            count = self.env['ir.ui.view'].search_count(
                ["|", ('arch', 'like', '"%s"' % url),
                 ('arch', 'like', "'%s'" % url)])
        self.website_file_count = count

    website_file = fields.Boolean('Website',
                                  help='Attachment available at website')
    website_file_count = fields.Integer('Number of uses',
                                        compute=_get_website_file_count)

    website_file_url = fields.Char('File url', compute=_get_website_file_url)

    # TODO do we need this in odoo 10.0?
    def try_remove_file(self):
        Views = self.env['ir.ui.view']
        attachments_to_remove = []
        # views blocking removal of the attachment
        removal_blocked_by = {}

        for attachment in self:
            # in-document URLs are html-escaped, a straight search will not
            # find them
            url = escape(attachment.website_file_url)
            views = Views.search(
                               ["|", ('arch', 'like', '"%s"' % url),
                                ('arch', 'like', "'%s'" % url)])

            for v in views:
                removal_blocked_by[v.id] = v.name  # probably incorrect update on porting
            else:
                attachments_to_remove.append(attachment.id)
        if attachments_to_remove:
            self.unlink(attachments_to_remove)
        return removal_blocked_by

    def check(self, mode, values=None):
        if self.ids and mode == 'read':
            ids = self.ids[:]  # copy
            self.env.cr.execute('SELECT id,website_file FROM ir_attachment WHERE id = ANY (%s)', (ids,))
            for id, website_file in self.env.cr.fetchall():
                if website_file:
                    ids.remove(id)
            if not ids:
                return
        return super(IrAttachment, self).browse(ids).check(mode, values)


class Website(models.Model):
    _inherit = 'website'

    def file_url(self, record, field='datas',
                 filename_field='datas_fname'):
        model = record._name
        # sudo_record = record.sudo()
        # hash_value = hashlib.sha1(sudo_record.write_date or sudo_record.create_date or '').hexdigest()[0:7]
        args = {
            'id': record.id,
            'model': model,
            'filename_field': filename_field,
            'field': field,
            # 'hash': hash_value,
        }
        return '/web/binary/saveas?%s' % werkzeug.url_encode(args)

    def search_files(self, needle=None,
                     limit=None):
        name = (needle or "")
        res = []
        res = self.env['ir.attachment'].search_read(domain=[
            ('website_file', '=', True),
            '|', ('datas_fname', 'ilike', name), ('name', 'ilike', name)
        ], fields=['datas_fname', 'website_file_url'], limit=limit)
        return res
