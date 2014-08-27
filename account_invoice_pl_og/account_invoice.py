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
import openerp.addons.decimal_precision as dp

#class account_invoice(osv.osv):
#    _inherit = 'account.invoice'
#    def line_get_convert(self, cr, uid, x, part, date, context={}):
#        res = super(account_invoice, self).line_get_convert(cr, uid, x, part, date, context)
#        res['asset_id'] = x.get('asset_id', False)
#        return res
#account_invoice()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns = {
        'original_inv_id': fields.many2one('account.invoice', 'Refunded Invoice', readonly = True, states={'draft':[('readonly',False)]}, help = "Invoice number of which this refund is based on."),
    }

    def refund(self, cr, uid, ids, date, period_id, description, journal_id):
        inv_obj = self.pool.get('account.invoice')
#        line_obj = self.pool.get('account.invoice.line')
        res = super(account_invoice, self).refund(cr, uid, ids, date, period_id, description, journal_id)
        new_id = res and res[0] or False
        if new_id:
            refund = inv_obj.browse(cr, uid, new_id)
            refund.write({
                'original_inv_id': ids[0],
                'type' : (refund.type in ['out_invoice','out_refund']) and 'out_refund' or 'in_refund',
            })
        return res

    def action_date_assign(self, cr, uid, ids, *args):
        inv_obj = self.pool.get('account.invoice')
        invoices = inv_obj.browse(cr, uid, ids)
#        raise osv.except_osv(_('Error !'), _('Refund invoice has to point to original invoice. Select Base Invoice No !'))
        for inv in invoices:
            if (inv.type in ('in_refund','out_refund')):
                if (inv.original_inv_id.id == False):
                    raise osv.except_osv(_('Error !'), _('Refund invoice has to point to original invoice. Select Base Invoice No !'))
                already_refund_id = inv_obj.search(cr, uid, [('original_inv_id','=',inv.original_inv_id.id),('state','in',['open','paid'])])
                if already_refund_id:
                    already_refund = inv_obj.browse(cr, uid, already_refund_id)
                    raise osv.except_osv(_('Error !'), _('Original invoice %s already has refund %s !')%(inv.original_inv_id.number,already_refund[0].number))                
        return super(account_invoice, self).action_date_assign(cr, uid, ids, *args)

    def _calc_net_gross(self, cr, uid, ids, context = None):
        tax_obj = self.pool.get('account.tax')
#        inv_lines_obj = self.pool.get('account.invoice.line')
        for invoice in self.browse(cr, uid, ids, context):
            for line in invoice.invoice_line:
                tax_value = 0.0
                u_price = line.quantity and line.price_subtotal/line.quantity or 0
                for tax in tax_obj.compute(cr, uid, line.invoice_line_tax_id, u_price, line.quantity, line.product_id, invoice.partner_id):
#                    tax_value = abs(tax['amount'])
                    tax_value = tax['amount']
                line.write({'invoice_line_tax': tax_value,'invoice_line_gross': tax_value + line.price_subtotal})
        return True


    def button_reset_taxes(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        super(account_invoice, self).button_reset_taxes(cr, uid, ids, context)
        self._calc_net_gross(cr, uid, ids, context = context)
        return True

    def action_move_create(self, cr, uid, ids, *args):
        super(account_invoice, self).action_move_create(cr, uid, ids, *args)
        self._calc_net_gross(cr, uid, ids)
        return True

account_invoice()

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'
    _columns = {
        'invoice_line_tax': fields.float("Tax", digits_compute= dp.get_precision('Account'), help = "Tax of invoice line.",),
        'invoice_line_gross': fields.float("Gross", digits_compute= dp.get_precision('Account'), help = "Gross of invoice line.",),
    }
account_invoice_line()

class account_invoice_tax(osv.osv):
    _inherit = 'account.invoice.tax'

    def _get_total(self, cr, uid, ids, *args):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id]=line.base + line.amount
        return res

    _columns = {
        'total_amount': fields.function(_get_total, method=True, store=True, string='Total', type="float", digits_compute= dp.get_precision('Account')),
    }
account_invoice_tax()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

