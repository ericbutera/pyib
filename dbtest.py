"""
[link]
url
netmask
createdDate

create table link (
    url TEXT,
    netmask VARCHAR(255),
    createdDate DATE
);

DATETIME('NOW')
"""

import sqlite3
con = sqlite3.connect("/home/eric/Aptana Studio Workspace/pyib/db/pyib.db");
c = con.cursor()

c.execute("""select * from link""");
for row in c:
    print row
    print repr(row)
con.close()
