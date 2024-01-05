import pymysql


class DIYMysql(object):
    def __init__(self, mysql_config):
        self.conn = pymysql.connect(
            host=mysql_config["HOST"],
            user=mysql_config["USER"],
            passwd=mysql_config["PASSWORD"],
            db=mysql_config["DATABASE"],
            charset='utf8'  # 根据实际可更改
        )

        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_fields_and_values(data_dict):
        fields = ""
        values = ""
        update_sql_str = ""
        for k, v in data_dict.items():
            fields += f"{k},"
            values += f"'{v}',"
            update_sql_str += f"{k}='{v}',"

        return fields[:-1], values[:-1], update_sql_str[:-1]

    def diy_write(self, table_name, query_condition, item):
        # 判断是否已存在数据库
        query_sql = "select * from %s where %s" % (table_name, query_condition)
        num = self.cursor.execute(query_sql)
        f, v, update_sql_str = self.create_fields_and_values(item)

        # 已存在则退出
        if num > 0:
            update_sql = "UPDATE %s SET %s where %s" % (table_name, update_sql_str, query_condition)
            # print(f"update_sql{update_sql}")
            self.cursor.execute(update_sql)
            self.conn.commit()
            return item

        # 不存在则写入Mysql
        insert_sql = "insert into %s (%s) values (%s)" % (table_name, f, v)
        self.cursor.execute(insert_sql)
        self.conn.commit()
        return item
