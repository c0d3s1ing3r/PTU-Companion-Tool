import psycopg2
import json
import traceback

conn = psycopg2.connect('dbname=postgres user=postgres password=password')

cur = conn.cursor()

class Table():

    def __init__(self, schema: str, name: str):
        self.schema : str = schema
        self.name : str = name
    
    def __str__(self) -> str:
        return self.schema + '.' + self.name
    
    def __repr__(self) -> str:
        return self.__str__()

class SimplePkeyValue():

    def __init__(self, pkey: str, data: str, table: str):
        self.pkey : str = pkey
        self.table = table
        try:
            data = data.replace('\n','\\n')
            self.data : dict = json.loads(data)
        except:
            print(pkey)
            print(data)
            print(table)
            traceback.print_exc()
            exit()
    
    def __str__(self) -> str:
        ret = self.table + ' -- ' + self.pkey + ' : ' + self.data.__str__()
        cutoff = -1
        if len(ret) >= cutoff and cutoff > 0:
            ret = ret[:cutoff]
        return ret
    
    def __repr__(self) -> str:
        return self.__str__()

cur.execute('select * from pg_catalog.pg_tables;')
tables = cur.fetchall()
tables = list(filter(lambda x: 'ptu' in x[1].lower() and 'ga' in x[1].lower(), tables))
tables = list(map(lambda x: Table(x[0], x[1]), tables))

    
for table in tables:
    print(table)
#exit()
def select_all(tbl: Table) -> list[SimplePkeyValue]:
    global cur
    cur.execute('select * from ' + tbl.__str__())
    ret = list(map(lambda x: SimplePkeyValue(x[0], x[1], tbl.__str__()), cur.fetchall()))
    return ret


table_data : list[list[SimplePkeyValue]] = []
for table in tables:
    if table.name == 'ptu_ga_pokemon' or table.name == 'ptu_ga_schema':
        tables.remove(table)
        continue
    table_data.append(select_all(table))

# table is in parallel to table_data
# table[i] corresponds to table_data[i]

print(tables[0])
for entry in table_data[0]:
    print('\t' + entry.pkey)
    for k, v in entry.data.items():
        print('\t\t{} : {}'.format(k, str(v)))

