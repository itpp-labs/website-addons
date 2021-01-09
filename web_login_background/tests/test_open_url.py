import odoo.tests


@odoo.tests.tagged("-at_install", "post_install")
class TestUi(odoo.tests.HttpCase):
    def test_open_url(self):
        # wait till page loaded
        code = """
            setTimeout(function () {
                if ($('body').css('background-image').startsWith('url')) {
                    console.log('test successful');
                } else {
                    console.log('test failed');
                }
            }, 3000);
        """
        link = "/web/login"
        self.browser_js(link, code)
