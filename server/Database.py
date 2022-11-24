import sqlite3
import subprocess


class Database():

    def __init__(self):
        # con = sqlite3.connect("database.db")    # Create connection to DB file
        # con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)    # Create connection to DB file
        con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        con.row_factory = sqlite3.Row
        self.db = con.cursor()                        # Create a cursor in the DB
        # self.db.mode("line")
        # subprocess.call(["sqlite3", "database.db", ".mode line"])



    def fetch(self, table, params, join=None):
        sql = f"""
            SELECT * 
            FROM '{table}'"""

        if join:
            sql += f""" 
            FULL JOIN '{join}' ON '{table}.user_id'='{join}.id'"""

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
        # msg = self.db.fetchall()
        msg = self.db.fetchone()

        # msg['user_id']

        print(f"Fetched data is:")
        print(msg.keys())
        print(msg)
        # dir(msg)
        # print(f"In fetch now from {table}")


    def fetch_group(self):
        print("Group fetching")






if __name__ == "__main__":
    db = Database()
    params = {'user_id': 1, 'group_id': 2}
    db.fetch("group_member", params, "user")
    db.fetch("group_member", params)
    # db.fetch_group()

