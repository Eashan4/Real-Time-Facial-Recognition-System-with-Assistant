import sqlite3

def print_user_table_schema():
    con = sqlite3.connect('data.db')
    cursor = con.cursor()
    cursor.execute("PRAGMA table_info(USER);")
    columns = cursor.fetchall()
    print("USER table schema:")
    for col in columns:
        print(col)
    con.close()

if __name__ == "__main__":
    print_user_table_schema()
