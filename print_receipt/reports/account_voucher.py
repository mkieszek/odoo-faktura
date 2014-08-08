# -*- coding: utf-8 -*-

import time
import pdb
from openerp.report import report_sxw
from openerp import pooler

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time': time,
                                  'getLines': self._lines_get,
                                  'blank_line' : self.blank_line,
                                  })
        self.context = context
           #generate blank lines/line break
    def blank_line(self, nlines):
       res = ""
       pdb.set_trace()
       for i in range(nlines - self.line_no):
          res = res + '\n'
       return res
   
   
    
    def _lines_get(self, voucher):
        voucherline_obj = pooler.get_pool(self.cr.dbname).get('account.voucher.line')
        voucherlines = voucherline_obj.search(self.cr, self.uid,[('voucher_id','=',voucher.id)])
        voucherlines = voucherline_obj.browse(self.cr, self.uid, voucherlines)
        return voucherlines
    
    
 
report_sxw.report_sxw('report.account_voucher', 'account.voucher',
                      'addons/print_receipt/reports/account_voucher.rml',
                      parser=Parser)
        