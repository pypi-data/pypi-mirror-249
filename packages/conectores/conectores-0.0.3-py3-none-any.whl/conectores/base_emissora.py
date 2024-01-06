
import psycopg2 as pg

def connect(table):
    try:
        conn = pg.connect(
            host = table[0], 
            database = table[0], 
            user = table[0], 
            password = table[0]
        )
    except:
        print('Erro! Sua conexão não foi estabilizada')
        conn = ''
    
    return conn

