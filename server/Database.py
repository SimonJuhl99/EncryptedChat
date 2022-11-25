import sqlite3
import subprocess


class Database():

    def __init__(self):
        # con = sqlite3.connect("database.db")    # Create connection to DB file
        # con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)    # Create connection to DB file
        con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        # con.row_factory = sqlite3.Row
        con.row_factory = self.dict_factory
        self.db = con.cursor()                        # Create a cursor in the DB
        # self.db.mode("line")
        # subprocess.call(["sqlite3", "database.db", ".mode line"])


    #  --  Function to create dictionary instead of list for fetched data
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def fetch(self, table, params, join=None):
        sql = f"""
            SELECT * 
            FROM '{table}'"""

        if join:
            sql += f""" 
            FULL OUTER JOIN '{join}' 
            ON '{table}.user_id'='{join}.id'"""

        for i, field in enumerate(params):
            if i>0:
                sql += """ 
            AND """
            else:
                sql += """
            WHERE """
            sql += f"""{field}={params[field]}"""


        print(f"SQL Statement is:\n{sql}")
        self.db.execute(sql)
        rows = self.db.fetchall()
        # rows = self.db.fetchone()


    ####################################
    ###  --  Test Printing Area  -- 

        print(f"Fetched data is:")
        for row in rows:
            # print(f"{row['id']} {row['name']} {row['price']}")
            print(f"{row}\n")

        # rows['user_id']
        # print(rows.keys())
        # print(rows)
        # dir(rows)
        # print(f"In fetch now from {table}")


    def fetch_group(self):
        print("Group fetching")


    def fetch_own_key(self, user_id):
        params = {'id': user_id}
        self.fetch('user', params)




if __name__ == "__main__":
    db = Database()
    # params = {'user_id': 1, 'group_id': 1}
    params = {'group_id': 1}
    # db.fetch("group_member", params, "user")
    # db.fetch("group_member", params)
    # db.fetch_group()
    db.fetch_own_key(3)

