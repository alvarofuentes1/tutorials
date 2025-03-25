{
    'name': 'Estate',
    'version': '1.0',
    'summary': 'Gestion de propiedades',
    'depends': ['base'],
    'data': 
    [
        #Security
        'security/ir.model.access.csv',
        #Views
        'views/real_estate_views.xml',
        'views/real_estate_menus.xml'
    ],
    'license': 'LGPL-3',
    'application': 'True',
    'installable': 'True'
}
