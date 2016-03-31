# -*- coding: utf-8 -*-
{
     'name': """Website sale checkout store""",
     'summary': """Select shipping and billing variants in web shop""",
     'category': 'Website',
     'images': [],
     'version': '1.0.0',

     'author': 'IT-Projects LLC',
     'website': 'https://it-projects.info',
     'license': 'GPL-3',
     #'price': 9.00,
     #'currency': 'EUR',

     'depends': [
         'website_sale',
     ],
     'external_dependencies': {'python': [], 'bin': []},
     'data': [
         'templates.xml',
         'views.xml',
     ],
     'demo': [
          'demo/demo.xml'
     ],
     'installable': True,
     'auto_install': False,
 }
