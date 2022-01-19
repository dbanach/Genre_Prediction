from DB_Manager import DB_Manager
def main():
    dbm = DB_Manager()

    sql_code = 'CREATE DATABASE auxiliar'
    # dbm.sql_command(sql_code)
    print(dbm.check_if_db_exists())

if __name__ == '__main__':
    main()