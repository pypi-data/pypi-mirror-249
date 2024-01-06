import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import os
import importlib

config_location = os.getenv("CONFIG_PATH", "KassOrm.configs.database")
connections = importlib.import_module(config_location).connections

class Conn:       
    
    def __init__(self, conn = None) -> None:    
        
        self.query = None          
        self.params = None           
        
        config_pool = connections['default'] if conn == None else connections[conn]        
        
        try:
            self.conn_pool = mysql.connector.pooling.MySQLConnectionPool(**config_pool)    
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
          
              
    def getQuery(self, query, params):
        self.query = query
        self.params = params
        return self
        
        
    def execute(self, fetchall = True):
        
        return self.execute_select(fetchall)
            
    
    def execute_select(self, fetchall = True):
        
        try:
            conn = self.conn_pool.get_connection()
                
            if conn and conn.is_connected():
                cursor = conn.cursor(dictionary=True, buffered=True)
                cursor.execute(self.query, params=self.params)                
            
                                
                if cursor.with_rows: 
                    result = cursor.fetchall() if fetchall == True else cursor.fetchone()                                                                   
                    cursor.close() 
                    conn.close()  
                  
                else:
                    result = None    
                
            else:
                print('Not connected. Check the credentials or the server')
                result = None
        
        except Exception as e:
            print(f"Error to catch data: {e}")
            result = None

        return result
        
        
    def execute_insert(self, many = False):
        
        conn = self.conn_pool.get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)
            
            if many:
                cursor.executemany(self.query, self.params)  
                
                lastid = cursor.lastrowid
                ultimos_ids = []
                x=0
                for _ in self.params:
                    id = lastid + x
                    ultimos_ids.append(id)
                    x=+1
            else:
                cursor.execute(self.query, params=self.params)  
                ultimos_ids = cursor.lastrowid
                
            conn.commit()           
            

            cursor.close()
            conn.close() 
            
        return ultimos_ids              
        
        
    def execute_update(self):
        try:
            conn = self.conn_pool.get_connection()
            if conn and conn.is_connected():
                cursor = conn.cursor(dictionary=True, buffered=True)

                cursor.execute(self.query, self.params)             
                    
                conn.commit()   

                cursor.close()
                conn.close() 
                
            return True    
        except Exception as err:
            return err 


    def execute_delete(self):
        conn = self.conn_pool.get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)

            cursor.execute(self.query, self.params)             
                
            conn.commit()   

            cursor.close()
            conn.close() 
            
        return True     


    def execute_create(self):
        conn = self.conn_pool.get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True, buffered=True)

            cursor.execute(self.query, self.params)             
                
            conn.commit()   

            cursor.close()
            conn.close() 
            
        return True   


    def __test_pool(self):
        try:
            # Criar várias conexões simultâneas
            for x in range(10):
                conn = self.conn_pool.get_connection()
                if conn and conn.is_connected():
                    print("Conexão obtida do pool com sucesso. " + str(x) )
                    # Realize operações na conexão se necessário                 
                    conn.close()  # Importante: fechar a conexão para devolvê-la ao pool
                else:
                    print("Não foi possível obter a conexão do pool.")

        except Exception as e:
            print(f"Erro ao testar o pool de conexões: {e}")

        finally:      
            # Certifique-se de fechar o pool de conexões após o teste
            conn_in_pool = self.conn_pool._remove_connections()
            print("Closed: " + str(conn_in_pool))