{
    'name': "L3 Module",
    'version': '1.0',
    'depends': ['base', 'sale', 'stock', 'sale_stock'],
    'author': "Ilya",
    'category': 'Category',
    'description': """
    Description text
    """,
    'data': [
        'views/res_partner_view.xml',
        'views/sale_extend_view.xml',
        'views/stock_picking_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
}
