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
        'views/real_estate_actions.xml',
        'views/real_estate_menus.xml',
        'views/real_estate_form.xml',
        'views/real_estate_search.xml',
        'views/real_estate_list.xml'
        
    ],
    'license': 'LGPL-3',
    'application': 'True',
    'installable': 'True'
}
