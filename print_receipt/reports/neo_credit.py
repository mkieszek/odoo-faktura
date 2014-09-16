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
                                  })
        self.context = context
   

 
report_sxw.report_sxw('report.neo_credit', 'neo.credit',
                      'addons/print_receipt/reports/schedule_print.rml',
                      parser=Parser, header=False)