# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>) 
#    All Rights Reserved
#    $Id$
#
#    Module account_invoice_pl_og is copyrighted by 
#    Grzegorz Grzelak of OpenGLOBE (www.openglobe.pl) and Cirrus (www.cirrus.pl)
#    with the same rules as OpenObject and OpenERP platform
#    All Rights reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "Poland - Localization of Invoices",
    "version" : "1.05 (7.0)",
    "author" : "Grzegorz Grzelak",
    "website": "http://www.openglobe.pl",
    "category" : "Localisation/Country specific stuff",
    "description": """
This is the module to manage Polish specific accounting functionality in Open ERP.
==================================================================================

To jest moduł do obsługi specyficznych księgowych wymagań funkcjonalnych
w Polsce.

Dodano:
-------
* Pola Podatek i Brutto do pozycji faktur
* Do faktury pole id faktury pierwotnej - stosowane do powiązania faktury korygującej z pierwotną
* Wydruk faktury sprzedażowej i sprzedażowej korygującej
* Widok partnerów po numerach NIP
    """,
    "depends" : ["account", "base_iban", "base_vat", "account_chart",

                ],
    "demo_xml" : [],
    "data" : [
#                    "account_menu.xml",
#                    "account_view.xml",
                    "report/invoice.xml",
                    "account_invoice_view.xml",
                    "partner_view.xml", 
                    "product_view.xml",
#                    "data/invoice_sequence.xml",
                    "data/account_data.xml",
                    "wizard/account_invoice_refund_view.xml",

                    ],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

