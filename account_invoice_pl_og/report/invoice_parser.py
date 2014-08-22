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
import pdb

def num2word(n,l="en_US"):
#    wordtable = ["zer","jed","dwa","trz","czt","pie","sze","sie","osi","dzi"]
    sym={
        "en_US": {
            "0": u'zero',
            "x": [u'one',u'two',u'three',u'four',u'five' ,u'six',u'seven',u'eight',u'nine'],
            "1x": [u'ten',u'eleven',u'twelve',u'thirteen',u'fourteen',u'fifteen',u'sixteen',u'seventeen',u'eighteen',u'nineteen'],
            "x0": [u'twenty',u'thirty',u'fourty',u'fifty',u'sixty',u'seventy',u'eighty',u'ninety'],
            "100": u'hundred',
            "1K": u'thousand',
            "1M": u'million',
        },
        "pl_PL": {
            "0": u'zero',
            "x": [u'jeden',u'dwa',u'trzy',u'cztery',u'pięć' ,u'sześć',u'siedem',u'osiem',u'dziewięć'],
            "1x": [u'dziesięć',u'jedenaście',u'dwanaście',u'trzynaście',u'czternaście',u'piętnaście',u'szesnaście',u'siedemnaście',u'osiemnaście',u'dziewiętnaście'],
            "x0":  [u'dwadzieścia',u'trzydzieści',u'czterdzieści',u'pięćdziesiąt',u'sześćdziesiąt',u'siedemdziesiąt',u'osiemdziesiąt',u'dziewięćdziesiąt'],
            "1xx": [u'sto',u'dwieście',u'trzysta',u'czterysta',u'pięćset',u'sześćset',u'siedemset',u'osiemset',u'dziewięćset'],
            "1000" : u'tysiąc',
            "1K": [u'tysięcy',u'tysięcy',u'tysiące',u'tysiące',u'tysiące',u'tysięcy',u'tysięcy',u'tysięcy',u'tysięcy',u'tysięcy', 'tysięcy'],
            "1M" : u'milion',
            "1Ms": [u'milionów',u'milionów',u'miliony',u'miliony',u'miliony',u'milionów',u'milionów',u'milionów',u'milionów',u'milionów'],
       }
    }

    if n==0:
        word = sym[l]["0"]
    elif n<10:
        word = sym[l]["x"][n-1]
    elif n<100:
        if n<20:
            word = sym[l]["1x"][n-10]
        else:
            word = sym[l]["x0"][n/10-2] + (n%10 and " " + num2word(n%10,l) or "")
    elif n<1000:
        if l=="en_US":
            word = sym[l]["x"][n/100-1]+" " + sym[l]["100"]+(n%100 and " "+num2word(n%100,l) or "")
        elif l=="pl_PL":
            word = sym[l]["1xx"][n/100-1] + (n%100 and " "+num2word(n%100,l) or "")
    elif n<1000000:
        if l=="en_US":
            word = num2word(n/1000,l)+" "+sym[l]["1K"]+(n%1000 and " "+num2word(n%1000,l) or "")
        elif l=="pl_PL":
            if n <2000:
                tys = sym[l]["1000"]
            elif n%100000>10000 and n%100000<20000:
                tys = sym[l]["1K"][0]
            else:
                tys = sym[l]["1K"][n/1000%10]
            word = num2word(n/1000,l) +" "+ tys + (n%1000  and " " + num2word(n%1000,l) or "")
    elif n<1000000000:
        if l=="en_US":
            word = num2word(n/1000000,l)+" "+sym[l]["1M"] + (n%1000000  and " " + num2word(n%1000000,l) or "")
        if l=="pl_PL":
            if n <2000000:
                mil = sym[l]["1M"]
            elif n%100000000>10000000 and n%100000000<20000000:
                mil = sym[l]["1Ms"][0]
            else:
                mil = sym[l]["1Ms"][n/1000000%10]
            word = num2word(n/1000000,l) +" "+ mil + (n%1000000  and " " + num2word(n%1000000,l) or "")
    else:
        return  "N/A"
    return word


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'invlines' : self.get_lines,
            'taxlines' : self.get_taxlines,
            'total' : self.get_total,
            'num2word' : self.get_word,
#            'currency2word' : self.get_word,
            'vatno' : self.get_vat_no,  # get Vat no without country code (like PL) when domestic customer.
            'invoice_address' : self.get_invoice_address,  # get Vat no without country code (like PL) when domestic customer.
        })

    def get_invoice_address(self, partner, *args):
        res = self.pool.get('res.partner').address_get(self.cr, self.uid, [partner.id], ['invoice'])
        return self.pool.get('res.partner.address').browse(self.cr, self.uid, res['invoice'],)

    def get_vat_no(self, partner, fiscal_position, *args):
        if not fiscal_position or fiscal_position.name == "Kraj":
            return partner.vat and partner.vat.lstrip('PL') or ''
        return partner.vat


    def get_word(self, r, l="pl_PL",*args):
        n= int(r)
        cents = " " +str(int(round((r - n) * 100))) +"/100"

        return num2word(n,l) + cents

    def get_total(self, inv_id, *args):
        invoice_obj = self.pool.get('account.invoice')
#        inv1_id = inv_id
        ret_list = {}
        res_list = []
        inv1 = invoice_obj.browse(self.cr, self.uid, inv_id)
        first_loop = True
        ret_list = {
                'amount_untaxed':0.0,
                'amount_tax':0.0,
                'amount_total':0.0,
                'residual':0.0,
                'new_amount_untaxed':0.0,
                'new_amount_tax':0.0,
                'new_amount_total':0.0,
                'new_residual':0.0,
        }
        while True:
            inv_prev = inv1.original_inv_id
            is_first = inv_prev and -1 or 1
            if (is_first == -1) and first_loop:
                ret_list['new_amount_untaxed'] = -inv1.amount_untaxed
                ret_list['new_amount_tax'] = -inv1.amount_tax
                ret_list['new_amount_total'] = -inv1.amount_total
            else:
                ret_list['amount_untaxed'] += inv1.amount_untaxed * is_first
                ret_list['amount_tax'] += inv1.amount_tax * is_first
                ret_list['amount_total'] += inv1.amount_total * is_first
            if not inv_prev:
                break
            else:
                inv1 = inv_prev
                first_loop = False

#        for key in ret_list.keys():
        if inv1.id != inv_id:
            ret_list['new_amount_untaxed'] += ret_list['amount_untaxed']
            ret_list['new_amount_tax'] += ret_list['amount_tax']
            ret_list['new_amount_total'] += ret_list['amount_total']
#        ret_list[key]['name'] = key
        res_list.append(ret_list)

        return res_list


    def get_lines(self, inv_id, *args):
        invoice_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')
        inv1_id = inv_id
        l=0
        while invoice_obj.browse(self.cr, self.uid, inv1_id).original_inv_id:
            inv1_id = invoice_obj.browse(self.cr, self.uid, inv1_id).original_inv_id.id
            l+=1
#        first_invoice = invoice_obj.browse(self.cr, self.uid, inv1_id)

        ret_list = {}
        res_list = []
        inv1 = invoice_obj.browse(self.cr, self.uid, inv1_id)
        if inv1.partner_id.lang:
            context={'lang': inv1.partner_id.lang}
            inv1 = invoice_obj.browse(self.cr, self.uid, inv1_id,context)

        first_loop = 1
        while True:
#            inv_prev = inv1.original_inv_id
#            is_first = inv_prev and -1 or 1
            seq = 0
            for line in inv1.invoice_line:
                prod_id = str(line.product_id.id)+line.name
                if not ret_list.has_key(prod_id):
                    seq += 1
                    name = ''
                    if line.invoice_line_tax_id and \
                            ((line.invoice_line_tax_id[0].tax_code_id and not line.invoice_line_tax_id[0].tax_code_id.notprintable) \
                            or (line.invoice_line_tax_id[0].base_code_id and not line.invoice_line_tax_id[0].base_code_id.notprintable)):
                        name = line.invoice_line_tax_id[0].description or line.invoice_line_tax_id[0].name
                    ret_list[prod_id] = {
                            'seq': seq,
                            'code':line.product_id and line.product_id.code or '',
                            'name':line.name,
                            'uos_name':line.uos_id.name,
                            'pkwiu' : line.product_id and line.product_id.pkwiu or '',
                            'tax_name': name,
                            'quantity': 0.0,
                            'price_unit' : 0.0,
                            'discount' : 0.0,
                            'price_subtotal' : 0.0,
                            'line_tax' : 0.0,
                            'line_gross' : 0.0,
                            'new_quantity' : 0.0,
                            'new_price_unit' : 0.0,
                            'new_discount' : 0.0,
                            'new_price_subtotal' : 0.0,
                            'new_line_tax' : 0.0,
                            'new_line_gross' : 0.0,
                    }

                if (inv1.id == inv_id) and (first_loop == -1):
                    ret_list[prod_id]['new_quantity'] = ret_list[prod_id]['quantity'] \
                                        - (((line.quantity != ret_list[prod_id]['quantity']) or \
                                        (line.quantity == ret_list[prod_id]['quantity']) and \
                                        (line.price_unit == ret_list[prod_id]['price_unit']) and \
                                        (line.discount == ret_list[prod_id]['discount'])) \
                                        and line.quantity or 0.0)
                    ret_list[prod_id]['new_price_unit'] = ret_list[prod_id]['price_unit'] \
                                        - ((line.price_unit != ret_list[prod_id]['price_unit']) and line.price_unit or 0.0)
                    ret_list[prod_id]['new_discount'] = ret_list[prod_id]['discount'] \
                                        - ((line.discount != ret_list[prod_id]['discount']) and line.discount or 0.0)
                    ret_list[prod_id]['new_price_subtotal'] = ret_list[prod_id]['price_subtotal'] - line.price_subtotal
                    ret_list[prod_id]['new_line_tax'] = ret_list[prod_id]['line_tax'] - line.invoice_line_tax
                    ret_list[prod_id]['new_line_gross'] = ret_list[prod_id]['line_gross'] - line.invoice_line_gross
                else:
                    ret_list[prod_id]['quantity'] += (line.quantity != ret_list[prod_id]['quantity']) and (line.quantity * first_loop) or 0.0
                    ret_list[prod_id]['price_unit'] += (line.price_unit != ret_list[prod_id]['price_unit']) and (line.price_unit * first_loop) or 0.0
                    ret_list[prod_id]['discount'] += (line.discount != ret_list[prod_id]['discount']) and (line.discount * first_loop) or 0.0
                    ret_list[prod_id]['price_subtotal'] += line.price_subtotal * first_loop
                    ret_list[prod_id]['line_tax'] += line.invoice_line_tax * first_loop
                    ret_list[prod_id]['line_gross'] += line.invoice_line_gross * first_loop
            if inv1.id == inv_id:
                break
            inv1_id = invoice_obj.search(self.cr, self.uid, [('original_inv_id','=',inv1.id)])
            inv1 = inv1_id and invoice_obj.browse(self.cr, self.uid, inv1_id[0]) or False
#            inv1 = inv_prev
            first_loop = -1

        for k in ret_list.keys():
            res_list.append(ret_list[k])

        return sorted(res_list, key=itemgetter('seq'))


    def get_taxlines(self, inv_id, *args):
        invoice_obj = self.pool.get('account.invoice')
        inv_taxline_obj = self.pool.get('account.invoice.tax')
#        inv1_id = inv_id
        ret_list = {}
        res_list = []
        inv1 = invoice_obj.browse(self.cr, self.uid, inv_id)
        first_loop = True
        while True:
            inv_prev = inv1.original_inv_id
            is_first = inv_prev and -1 or 1
            for line in inv1.tax_line:
                if ((line.tax_code_id and line.tax_code_id.notprintable)
                    or (line.base_code_id and line.base_code_id.notprintable)):
                    continue
                if not ret_list.has_key(line.name):
                    ret_list[line.name] = {
                            'base':0.0,
                            'amount':0.0,
                            'total_amount':0.0,
                            'new_base':0.0,
                            'new_amount':0.0,
                            'new_total_amount':0.0,
                    }
                if (is_first == -1) and first_loop:
                    ret_list[line.name]['new_base'] = line.base * is_first
                    ret_list[line.name]['new_amount'] = line.amount * is_first
                    ret_list[line.name]['new_total_amount'] = line.total_amount * is_first
                else:
                    ret_list[line.name]['base'] += line.base * is_first
                    ret_list[line.name]['amount'] += line.amount * is_first
                    ret_list[line.name]['total_amount'] += line.total_amount * is_first
            if not inv_prev:
                break
            else:
                inv1 = inv_prev
                first_loop = False

        for key in ret_list.keys():
            if inv1.id != inv_id:
                ret_list[key]['new_base'] += ret_list[key]['base']
                ret_list[key]['new_amount'] += ret_list[key]['amount']
                ret_list[key]['new_total_amount'] += ret_list[key]['total_amount']
            ret_list[key]['name'] = key
            res_list.append(ret_list[key])

        return res_list

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
