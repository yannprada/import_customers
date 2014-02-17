# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class CustomerManager(Manager):
    def __init__(self, host, dbname, password):
        super(CustomerManager, self).__init__(host, dbname, password)
        self.existing_partners_records = self.prepare_ir_model_data('res.partner')
        title_records = self.prepare_many2one('res.partner.title')
        country_records = self.prepare_many2one('res.country')
        self.fieldsNames = {
            'title': {'fieldName': 'title', 'records': title_records},
            'country': {'fieldName': 'country', 'records': country_records},
            'name': 'name',
            'street': 'street',
            'zip': 'zip',
            'city': 'city',
            'phone': 'phone',
            'mobile': 'mobile',
            'fax': 'fax',
            'email': 'email',
            'website': 'website',
            'customer': 'customer',
            'is_company': 'is_company',
        }
    
    def run(self, fileName):
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = {}
            for key in self.fieldsNames:
                value = self.fieldsNames[key]
                if type(value) == dict:
                    data[key] = value['records'][row[value['fieldName']]]
                else:
                    data[key] = row[value]
            ref = row['ref']
            ID = self.insertOrUpdate(ref,'res.partner', data, self.existing_partners_records)
            
            if __name__ == '__main__':
                print(str(count) + ' --- ID: ' + str(ID))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
Usage:
    python insert.py [host] [database] [password] [file.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        cm = CustomerManager(sys.argv[1], sys.argv[2], sys.argv[3])
        cm.run(sys.argv[4])
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

