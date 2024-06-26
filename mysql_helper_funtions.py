import os
from dotenv import load_dotenv

from sqlalchemy import create_engine , text


# Load environment variables from .env file
load_dotenv(dotenv_path='./.env')
def get_connection():
    
    engine = create_engine("mysql+mysqlconnector://root:root@localhost:3307")
    return engine
    

def create_db():
    engine = get_connection()
    with engine.connect() as  connection:
        
        connection.execute(text("""CREATE database IF NOT EXISTS stocks;"""))
        connection.execute(text("""CREATE TABLE IF NOT EXISTS stocks.stocks_master(
                        stock_mstr_key SMALLINT auto_increment primary key,
                        stock_name VARCHAR(50),
                        org_name VARCHAR(250),
                        start_date DATE,
                        end_date DATE,
                        last_updated DATE
                        );"""))
        connection.execute(text("""CREATE TABLE IF NOT EXISTS `stock_data` (
                                    `Date` date NOT NULL,
                                    `Open` double DEFAULT NULL,
                                    `High` double DEFAULT NULL,
                                    `Low` double DEFAULT NULL,
                                    `Close` double DEFAULT NULL,
                                    `Adj Close` double DEFAULT NULL,
                                    `Volume` bigint DEFAULT NULL,
                                    `stock_mstr_key` bigint NOT NULL,
                                    PRIMARY KEY (`stock_mstr_key`,`Date`),
                                    KEY `idx_stock_mstr_key` (`stock_mstr_key`)
                                    );"""))
        print("Schema Created")
        connection.close()

def insert_new_stock(stock_name,org_name,start_date,end_date,last_updated):
     
     engine =  get_connection()
     with engine.connect() as connection:
        query = "INSERT INTO stocks.stocks_master(stock_name,org_name,start_date,end_date,last_updated) \
                        VALUES('"+str(stock_name)+"','"+str(org_name)+"','"+str(start_date)+"','"+str(end_date)+"','"+str(last_updated)+"');"
        connection.execute(text(query))
        connection.commit()
        print(stock_name+" inserted into Stock Master")
        connection.close()

def get_stock_mstr_key(stock_name):
    
    engine = get_connection()
    with engine.connect() as connection :
        query = "SELECT s.stock_mstr_key FROM stocks.stocks_master s WHERE s.stock_name = '"+stock_name+"';"
        result =  connection.execute(text(query)).fetchone()
        connection.close()
        return result[0]
    
def get_current_end_date(stock_name):
    
    engine = get_connection()
    with engine.connect() as connection :
        query = "SELECT s.end_date FROM stocks.stocks_master s WHERE s.stock_name = '"+stock_name+"';"
        result =  connection.execute(text(query)).fetchone()
        connection.close()
        return result[0]

def update_stock_end_date(stock_name,end_date):
    
    engine = get_connection()
    with engine.connect() as connection :
        query = "UPDATE stocks.stocks_master s SET s.end_date = '"+str(end_date)+"' WHERE s.stock_name = '"+stock_name+"';"
        connection.execute(text(query))
        connection.commit()
        connection.close()
        return 'Record Updated'
     

if __name__ == '__main__':
        engine = get_connection()
        with engine.connect() as connection:
            create_db()
            connection.close()
        
    