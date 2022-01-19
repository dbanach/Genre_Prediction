import config as cf
import pymysql

class DB_Manager():


    def __init__(self):
        """
        the constructor of the class. It creates the Database if it does not exist and creates the tables.
        """

        cursor = pymysql.cursors.DictCursor
        connection = pymysql.connect(host=cf.DB_IP, user=cf.DB_USER, password=cf.DB_PASS,charset=cf.CHARSET, cursorclass=cursor)

        self.connection = connection

    def check_if_db_exists(self):
        '''
        function that returns True if Movies database is already created, False if not
        '''
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        schemas = cursor.fetchall()

        cursor.close()

        schemas = [ my_dict['Database'] for my_dict in schemas]

        if cf.DATABASENAME in schemas:
            return True
        else:
            return False

    def sql_command(self,sql_code):

        cursor = self.connection.cursor()
        cursor.execute(sql_code)

        cursor.close()

    def build_db(self):
        '''
        Function that builds the database and it's table structure
        '''

        if not self.check_if_db_exists():
            sql_code = f'CREATE DATABASE {cf.DATABASENAME}'
            self.sql_command(sql_code)
            sql_code = f'Use {cf.DATABASENAME}'
            self.sql_command(sql_code)

            sql_code = """  CREATE TABLE IF NOT EXISTS Movies (movie_id int AUTO_INCREMENT
                                            ,name varchar(100) NOT NULL
                                            ,summary text NOT NULL
                                            ,synopsis text NOT NULL 
                                        ,PRIMARY KEY (movie_id))    
                                        """
            self.sql_command(sql_code)

    def insert(self,movie_name,summary,synopsis):
        sql_code = f'Use {cf.DATABASENAME}'
        self.sql_command(sql_code)
        sql_code = f"""INSERT IGNORE INTO Movies (name, summary,synopsis) VALUES ('{movie_name}', '{summary}','{synopsis}')"""
        print(sql_code)

        self.sql_command(sql_code)
        self.connection.commit()