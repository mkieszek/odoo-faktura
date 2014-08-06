# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
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

from openerp.osv import osv, fields
from openerp.tools import config
import time
from openerp.tools.translate import _
#import netsvc


class account_tax(osv.osv):
    _inherit = 'account.tax'

    # to return tax code only instead of code + name 
    def _unit_compute(self, cr, uid, taxes, price_unit, product=None, partner=None, quantity=0):
        res = super(account_tax, self)._unit_compute(cr, uid, taxes, price_unit, product, partner, quantity)
        for i in range(len(res)):
            tax = self.pool.get('account.tax').browse(cr, uid, res[i]['id'])
            res[i].update({'name':tax.description or tax.name})
        return res
account_tax()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

