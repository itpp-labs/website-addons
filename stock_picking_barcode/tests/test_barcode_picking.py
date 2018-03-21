import odoo.tests
# from odoo.api import Environment


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestBarcodePickingUi(odoo.tests.HttpCase):

    def test_stock_picking_barcode(self):

        # env = Environment(self.registry.test_cr, self.uid, {})
        # env['res.partner'].search([('id', '=', 9)]).debt_limit = 100

        # without a delay there might be problems on the steps whilst opening a POS
        # caused by a not yet loaded button's action
        self.phantom_js("/web",
                        "odoo.__DEBUG__.services['web_tour.tour'].run('tour_stock_picking_barcode', 1000)",
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.tour_stock_picking_barcode.ready",
                        login="admin")
