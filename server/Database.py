import sqlite3


class Database():

    def __init__(self):
        con = sqlite3.connect("database.db")    # Create connection to DB file
        db = con.cursor()                        # Create a cursor in the DB


    def fetch(self, table, param):
        sql = f"""
            SELECT * 
            FROM {table}
            WHERE user_id = {param}"""
        
        print(f"In fetch now from {table}")
        print(f"SQL Statement is:\n{sql}")

    def fetch_group(self):
        print("Group fetching")






if __name__ == "__main__":
    db = Database()
    db.fetch("group_member", "1")
    db.fetch_group()

