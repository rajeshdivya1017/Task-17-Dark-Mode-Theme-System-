import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="$Divya@1010",  
        database="ecommerce"
    )