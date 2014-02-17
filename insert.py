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
        self.title_records = self.prepare_many2one('res.partner.title')
        self.country_records = self.prepare_many2one('res.country')
        self.title_records[''] = False
        self.country_records[''] = False
    
    def run(self, fileName):
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = {
                'title': self.title_records[row['title']],
                'name': row['name'],
                'street': row['street'],
                'zip': row['zip'],
                'city': row['city'],
                'country': self.country_records[row['country']],
                'phone': row['phone'],
                'mobile': row['mobile'],
                'fax': row['fax'],
                'email': row['email'],
                'website': row['website'],
                'customer': row['customer'],
                'is_company': row['is_company'],
            }
            ref = row['ref']
            ID = self.insertOrUpdate(
                    ref,'res.partner', data, self.existing_partners_records)
            
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

