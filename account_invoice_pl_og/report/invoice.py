# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    Module account_invoice_pl_og is copyrighted by 
#    Grzegorz Grzelak of OpenGLOBE (www.openglobe.pl) and Cirrus (www.cirrus.pl)
#    with the same rules as OpenObject and OpenERP platform
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

import time
from openerp.report import report_sxw

from openerp.osv import osv, fields
from openerp.tools.translate import _
from operator import itemgetter, attrgetter
from invoice_parser import Parser

report_sxw.report_sxw(
    'report.account_invoice_pl_og.invoice_cirrus',
    'account.invoice',
    'addons/account_invoice_pl_og/report/invoice.rml',
    parser = Parser  # account_invoice
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
