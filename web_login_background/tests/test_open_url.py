# -*- coding: utf-8 -*-
import logging

from odoo.tests.common import HttpCase

_logger = logging.getLogger(__name__)


class TestDataGet(HttpCase):
    at_install = True
    post_install = True

    def test_open_url(self):
        url = '/web/login'
        self.url_open(url)
