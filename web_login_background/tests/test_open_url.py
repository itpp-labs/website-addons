# -*- coding: utf-8 -*-
import logging

from odoo.tests.common import HttpCase

_logger = logging.getLogger(__name__)


class TestDataGet(HttpCase):
    at_install = True
    post_install = True

    def test_open_url(self):
        user_demo = self.env.ref('base.user_demo')
        url = '/web/image?model=res.users&id={}&field=image_medium'.format(user_demo.id)

        self.url_open(url)
