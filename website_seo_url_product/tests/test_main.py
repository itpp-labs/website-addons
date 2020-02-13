from odoo.tests.common import TransactionCase


class TestWebsiteSeoUrlProduct(TransactionCase):
    post_install = True

    def setUp(self):
        super(TestWebsiteSeoUrlProduct, self).setUp()
        self.product1 = self.env.ref("product.product_product_1")
        self.product2 = self.env.ref("product.product_product_2")

    def test_10_seo_url_checking(self):
        SEO_URL_VALUE = "some-seo-url"

        # should be no duplicated SEO URLs
        vals = {"seo_url": SEO_URL_VALUE}
        self.product1.write(vals)
        self.product2.write(vals)
        self.assertEqual(
            1,
            self.env["product.product"].search_count([("seo_url", "=", SEO_URL_VALUE)]),
        )
