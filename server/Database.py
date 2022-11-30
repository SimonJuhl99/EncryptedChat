import sqlite3
import subprocess


class Database():

    def __init__(self):

        self.con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory    # Make dictionaries instead of lists
        self.cur = self.con.cursor()        # Create a cursor in the DB


    #  --  Function to create dictionary instead of list for fetched data
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d



##########################################
##  --  Fetch Area --
############

    ######################################
    #  --  General fetch function  --
    def fetch(self, table, setup = None):
        # print(setup)

        self.con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


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
            FROM '{table}'"""

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


        # print(f"\nSQL Statement is:{sql}\n\n")
        self.cur.execute(sql)
        # print("Efter Execute")
        rows = self.cur.fetchall()
        # print("Efter Fetch All")
        # rows = self.cur.fetchone()


    ####################################
    ###  --  Test Printing Area  -- 

        print(f"Fetched data is:")
        for row in rows:
            print(f"{row}")

        return rows


    # Function to fetch group members
    def fetch_group_members(self, group_id):
        # print("Group fetching")
        db_config = {'where': {'group_member.group_id': group_id},
            'select': 'group_member.user_id, group_member.admin, user.alias, user.ip',
            'join':{'user': 'group_member.user_id=user.id'}
            }
        
        return self.fetch('group_member', db_config)


    # Fetch your own user info
    def fetch_own_key(self, user_id):
        db_config = {'where':{'id': user_id}}
        return self.fetch('user', db_config)




##########################################
##  --  Insert Area --
############

    ######################################
    #  --  General fetch function  --
    def insert(self, table, params):

        self.con = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES)    # Create connection to DB file
        self.con.row_factory = self.dict_factory
        self.cur = self.con.cursor()


        sql = f"""
            INSERT INTO {table}
            ("""

        sql_end = ""


        for i, key in enumerate(params):

            if i>0:     # If not first column
                sql += ", "
                sql_end += ", "
            
            sql += f"{key}"

            sql_end += f"'{params[key]}'"

        sql += f""")
            VALUES ({sql_end})"""


        # print(f"\nSQL Statement is:{sql}\n\n")
        self.cur.execute(sql)
        self.con.commit()

        print(f"Last Inserted Row is: {self.cur.lastrowid}")

        return self.cur.lastrowid


    # Method to log messages to database
    def insert_msg(self, text, user_id, group_id):
        params = {'text': text, 'user_id': user_id, 'group_id': group_id}
        return self.insert('message', params)



if __name__ == "__main__":
    db = Database()

    # Fetch Testing
    db.fetch('user')

    db.fetch_group_members(1)
    db.fetch_own_key(3)


    # Insert Testing
    db.insert('message', {'text': 'ting er grimme', 'user_id': 2, 'group_id': 1})

    db.insert_msg('næste besked', 1, 2)