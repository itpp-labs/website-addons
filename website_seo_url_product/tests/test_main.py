# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase


class TestWebsiteSeoUrlProduct(TransactionCase):
    post_install = True

    def setUp(self):
        super(TestWebsiteSeoUrlProduct, self).setUp()
        cr, uid = self.cr, self.uid
        self.ir_model_data = self.registry('ir.model.data')
        self.usb_adapter_id = self.ir_model_data.get_object_reference(cr, uid, 'product', 'product_product_48')[1]
        self.datacard_id = self.ir_model_data.get_object_reference(cr, uid, 'product', 'product_product_46')[1]

    def test_10_seo_url_checking(self):
        cr, uid, context = self.cr, self.uid, {}
        SEO_URL_VALUE = 'some-seo-url'

        # should be no duplicated SEO URLs
        self.registry('product.product').write(cr, uid, [self.usb_adapter_id, self.datacard_id], {'seo_url': SEO_URL_VALUE}, context=context)
        self.assertEqual(1, self.registry('product.product').search_count(cr, uid, [('seo_url', '=', SEO_URL_VALUE)], context=context))
