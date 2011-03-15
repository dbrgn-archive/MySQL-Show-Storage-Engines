#!/usr/bin/env python

# Show/list the storage engine of all database tables on the local MySQL server
# Author: Danilo Bargen
# License: GPLv3

import MySQLdb
import re
import getpass

pw = getpass.getpass('MySQL root password: ').strip()
db = MySQLdb.connect('localhost', 'root', pw)
cursor = db.cursor()

cursor.execute('SHOW DATABASES')
databases = [r[0] for r in cursor.fetchall()]
engine_count = dict()
separator = '-' * 40

for d in databases:
    print separator
    print 'DB: %s' % d
    cursor.execute('USE %s' % d)
    cursor.execute('SHOW TABLES')
    tables = [r[0] for r in cursor.fetchall()]
    for t in tables:
        cursor.execute('SHOW CREATE TABLE %s' % t)
        create_statement = cursor.fetchall()[0][1]
        engine = re.search(r'ENGINE=(\w+) ', create_statement).group(1)
        print 'Table %s: %s' % (t, engine)
        try:
            engine_count[engine] += 1
        except KeyError:
            engine_count[engine] = 1

print '\n' + separator + '\nSUMMARY\n' + separator
for i in engine_count.items():
    print '%s: %u' % i
