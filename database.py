import sqlite3

class SQLiteHelper:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, fields):
        """
        创建表
        :param table_name: 表名
        :param fields: 字段列表，格式为 [(fieldname, type), ...]
        :return: None
        """
        fields_str = ', '.join([f'{f[0]} {f[1]}' for f in fields])
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})'
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name, fields, values):
        """
        插入数据
        :param table_name: 表名
        :param fields: 字段列表，格式为 [fieldname1, fieldname2, ...]
        :param values: 值列表，格式为 [(value1, value2, ...), ...]
        :return: None
        """
        fields_str = ', '.join(fields)
        placeholders_str = ', '.join(['?' for _ in range(len(fields))])
        sql = f'INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders_str})'
        # print(sql)
        self.cursor.executemany(sql, values)
        self.conn.commit()

    def update(self, table_name, set_fields, condition_fields=None):
        """
        更新数据
        :param table_name: 表名
        :param set_fields: 要更新的字段和值，格式为 {fieldname1: value1, fieldname2: value2, ...}
        :param condition_fields: 更新条件，格式为 {fieldname1: value1, fieldname2: value2, ...}
        :return: None
        """
        set_fields_str = ', '.join([f'{k}=?' for k in set_fields])
        sql = f'UPDATE {table_name} SET {set_fields_str}'
        if condition_fields:
            condition_fields_str = ' AND '.join([f'{k}=?' for k in condition_fields])
            sql += f' WHERE {condition_fields_str}'
        self.cursor.execute(sql, tuple(set_fields.values()) + tuple(condition_fields.values()))
        self.conn.commit()

    def delete(self, table_name, condition_fields):
        """
        删除数据
        :param table_name: 表名
        :param condition_fields: 删除条件，格式为 {fieldname1: value1, fieldname2: value2, ...}
        :return: None
        """
        condition_fields_str = ' AND '.join([f'{k}=?' for k in condition_fields])
        sql = f'DELETE FROM {table_name} WHERE {condition_fields_str}'
        self.cursor.execute(sql, tuple(condition_fields.values()))
        self.conn.commit()

    def query(self, table_name, fields=None, condition_fields=None):
        """
        查询数据
        :param table_name: 表名
        :param fields: 要查询的字段列表，格式为 [fieldname1, fieldname2, ...]，默认为全部字段
        :param condition_fields: 查询条件，格式为 {fieldname1: value1, fieldname2: value2, ...}
        :return: 查询结果，每行数据以字典形式返回
        """
        if fields:
            fields_str = ', '.join(fields)
        else:
            fields_str = '*'
        sql = f'SELECT {fields_str} FROM {table_name}'
        if condition_fields:
            condition_fields_str = ' AND '.join([f'{k}=?' for k in condition_fields])
            sql += f' WHERE {condition_fields_str}'
            results = self.cursor.execute(sql, tuple(condition_fields.values()))
        else:
            results = self.cursor.execute(sql)
        rows = results.fetchall()
        if not rows:
            return []
        columns = [c[0] for c in results.description]
        return [dict(zip(columns, row)) for row in rows]
    def execute_sql(self,sql):
        # 执行SQL查询语句
        self.cursor.execute(sql)
        # 获取查询结果
        result = self.cursor.fetchall()
        # 返回查询结果
        return result
    def execute_sql_with_description(self,sql):
        # 执行SQL查询语句
        results = self.cursor.execute(sql)
        # 获取查询结果
        rows = self.cursor.fetchall()
        columns = [c[0] for c in results.description]
        return [dict(zip(columns, row)) for row in rows]

    def delete_duplicates(self,delete_sql):
        """
        Delete duplicate records from a SQLite database.

        :param db_file: The path to the SQLite database file.
        :param delete_sql: The SQL command to delete duplicate records.
        :return: The number of rows deleted.
        """
        self.cursor.execute(delete_sql)
        rows_deleted = self.cursor.rowcount
        # 提交更改并关闭连接
        self.conn.commit()
        # 返回删除的行数
        return rows_deleted
    def close(self):
        """
        关闭连接
        :return: None
        """
        self.cursor.close()
        self.conn.close()