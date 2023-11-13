from flask import g, current_app as app
import pandas as pd


class dbProcess:

    def __init__(self, table_name, select_column_list=[], val_dict_data={}, where_dict_data={}):
        self.db_conn_cur = g.db['dbConnCur']
        self.db_conn_eng = g.db['dbConnEng']
        self.table = table_name
        self.column_list = select_column_list
        self.val_dict_data = val_dict_data
        self.where_dict_data = where_dict_data

    def select_query(self):
        response = dict({"status": "success", "message": "query executed successfully"})
        try:
            if self.column_list:
                columns = ', '.join(self.column_list)
            else:
                columns = ' * '

            if self.where_dict_data:
                where_stm = ' WHERE {}'.format(' AND '.join('{}=%s'.format(k) for k in self.where_dict_data))
            else:
                where_stm = ''

            sql = "SELECT %s FROM %s " % (columns, self.table)

            query = sql + where_stm

            self.db_conn_cur.execute(query, list(self.where_dict_data.values()))
            result = self.db_conn_cur.fetchall()
            response['result'] = result

        except Exception as e:
            app.logger.error(f'Exception - {format(e)}')
            response = {"status": "failure", "message": format(e)}
        finally:
            return response

    def insert_query(self):
        try:
            placeholders = ', '.join(['%s'] * len(self.val_dict_data))
            columns = ', '.join(self.val_dict_data.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (self.table, columns, placeholders)

            self.db_conn_cur.execute(sql, list(self.val_dict_data.values()))

        except Exception as e:
            app.logger.error(f'Exception - {format(e)}')
            response = {"status": "failure", "message": format(e)}

        return