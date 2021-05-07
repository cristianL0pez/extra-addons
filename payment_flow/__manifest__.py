# -*- coding: utf-8 -*-

{
    'name': 'Flow Payment Acquirer',
    'category': 'Payment / Chile',
    'author': 'Daniel Santibáñez Polanco',
    'summary': 'Payment Acquirer: Chilean Flow Payment Acquirer',
    'website': 'https://globalresponse.cl',
    'version': "0.7.0",
    'description': """Chilean Flow Payment Acquirer""",
    'depends': [
            'payment',
            'payment_currency',
    ],
    'external_dependencies': {
            'python': [
                'payflow',
            ],
    },
    'data': [
        'views/flow.xml',
        'views/payment_acquirer.xml',
        'views/payment_transaction.xml',
        'data/flow.xml',
    ],
    'installable': True,
    'application': True,
}
