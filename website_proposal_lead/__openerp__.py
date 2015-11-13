{
    'name' : 'Website proposal for leads',
    'version' : '1.0.0',
    'author' : 'IT-Projects LLC, Ivan Yelizariev',
    'license': 'GPL-3',
    'category' : 'Base',
    'website' : 'https://yelizariev.github.io',
    'description': """
Web-based proposals for leads
    """,
    'depends' : ['website_proposal', 'crm', 'sale_crm', 'sale',],
    'data':[
        'views.xml',
        'report.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
