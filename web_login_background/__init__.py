# -*- coding: utf-8 -*-
import controllers
import models
from openerp import SUPERUSER_ID
import openerp.tools as tools

def init_web_login_background(cr, registry):
    if tools.config['without_demo']:
        return
    icp = registry['ir.config_parameter']
    icp.set_param(cr, SUPERUSER_ID, 'auth_signup.allow_uninvited', True)

