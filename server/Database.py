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


    # def fetch(self, table, params=None, join=None):
    def fetch(self, table, setup = None):
        # print(table)
        # print(setup)

        # Default fetch config
        config = {'select': '*', 
            'where': None,
            'join': None}

        # Replace defaults with set settings, if any exists
        if setup:
            config = dict(list(config.items()) + list(setup.items()))

        # print(config)

        sql = f"""
            SELECT {config['select']} 
            FROM {table}"""

        if config['join']:
            keys = list(config['join'].keys())

            for i, key in enumerate(config['join']):
                sql += f""" 
            FULL OUTER JOIN {keys[i]} 
            ON {config['join'][key]}"""


        if config['where']:
            for i, key in enumerate(config['where']):

                if i>0:     # If not first column
                    sql += """ 
            AND """

                else:       # If first column
                    sql += """
            WHERE """
                
                sql += f"""{key}={config['where'][key]}"""


        print(f"SQL Statement is:\n{sql}\n\n")
        self.db.execute(sql)
        rows = self.db.fetchall()
        # rows = self.db.fetchone()


    ####################################
    ###  --  Test Printing Area  -- 

        print(f"Fetched data is:")
        for row in rows:
            print(f"{row}")


    # Function to fetch group members
    def fetch_group_members(self, group_id):
        print("Group fetching")
        db_config = {'where': {'group_member.group_id': group_id},
            'select': 'group_member.admin, user.alias',
            'join':{'user': 'group_member.user_id=user.id'},
            }
        
        self.fetch('group_member', db_config)

    # Fetch your own user info
    def fetch_own_key(self, user_id):
        db_config = {'where':{'id': user_id}}
        self.fetch('user', db_config)




if __name__ == "__main__":
    db = Database()
    db_config = {'where': {'group_id': 1}}
    # db.fetch("group_member", db_config)

    # db_config = {'user_id': 1, 'group_id': 1}
    # db.fetch("group_member", db_config)

    db.fetch('user')

    db.fetch_group_members(1)
    db.fetch_own_key(3)

