import json
from .Conn import Conn
from datetime import datetime
import os, importlib

config_location = os.getenv("CONFIG_PATH", "KassOrm.configs.database")

useSofdelete = importlib.import_module(config_location).useSofdelete

class Querier:
    
    def __init__(self, conn=None, softDelete = False) -> None:   
        
        self.__conn = Conn(conn) 
        
        __useSoftDelete = useSofdelete['default'] if conn == None else useSofdelete[conn]     
        
        self.__softDelete = False if softDelete == None else softDelete if softDelete != False else __useSoftDelete
        
        self.__withTrashed = False
        
        self.__params = {}    
        
        self.__columns = [{"name":"*"}]
        
        self.__not_columns = []
        
        self.__table = None
        
        self.__table_alias = None
        
        self.__limit = None
        
        self.__offset = None
    
        self.__group = None 
               
        self.__order = None        
        
        self.__conditional = []
        
        self.__SQL = ""        
        
        self.__values_update = None
        
        self.__last_method = 'select'
        
        self.__join = []
        
        self.__queries = []
    
       
    # raw---------------------------------------------------------------
    def raw(self, query:str, params:dict = {}, all:bool = True):        
        result =  self.__conn.getQuery(query,params).execute(all)      
        data = json.dumps(result, default=self.__convert_datetime_to_string)    
        return data    
    
    
    #select-------------------------------------------------------------
    
    def select(self, columns:list[str|dict]):
        """Informar quais colunas buscar""" 
        
        self.__columns = []
    
        for col in columns:
            
            if type(col) == dict:
                self.__columns.append(col) 
            else:
                self.__columns.append({"name":col}) 
            
        return self
    
    
    def notSelect(self, columns:list[str]):
        self.__not_columns = []
    
        for col in columns:  
            self.__not_columns.append(col) 
            
        return self
        
    
    def table(self, table:str, alias:str = None):
        """Informa a table e seu alias se houver"""
                
        self.__table = table
        
        self.__table_alias = alias
        
        # self.__columns = self.__getColumnsNames(self.__table, alias)
        
        return self
    
    
    def withTrashed(self):
        self.__withTrashed = True
        return self
    
    
    
    
    #joins-------------------------------------------------------------
        
    # def join(self, table, model_key, local_key):
    #     self.__join.append(f" LEFT JOIN {table} ON ({table}.{model_key} = {self.__table}.{local_key}) ")    
    #     return self
    
    
    
    
    # condicional-------------------------------------------------------------
        
    def where(self, values:dict, conector:str = 'AND'):
                
        where = ""     
               
        for col, value in values.items():
            keyParamValue, keyParam = self.__paramKey(col)
            self.__params[keyParamValue] = value
            
            where += f" {col} = {keyParam} AND "
            
        where = where[:-4]    
            
        self.__conditional.append({"where":where, "conector":conector})    
        return self
            
    
    def whereIn(self, column:str, values:list[str], conector:str = "AND", type:str = ''):
        
        where = f"{column} {type} IN "
        
        vals = ''
        for index, val in enumerate(values):
            keyParamValue, keyParam = self.__paramKey(f"{column}in{index}")
            self.__params[keyParamValue] = val
        
            vals += f"'{keyParam}', "
            
        where += f"({vals[:-2]})"        
    
        self.__conditional.append({"where":where, "conector":conector})    
        return self
    
    
    def whereNotIn(self, column:str, values:list[str], conector = 'AND'):
        
        return self.whereIn(column=column, values=values, type="NOT", conector=conector)  
    
    
    def orWhere(self, values:dict):
        
        return self.where(values, "OR")
    
    
    def orWhereIn(self, column:str, values:list[str]):
        
        return self.whereIn(column, values, "OR")
            
    
    def whereIsNull(self, column, conector:str = 'AND', type:str=""):        

        where = f" {column} IS {type} NULL "    
        self.__conditional.append({"where":where, "conector":conector})    
        return self
    
    
    def whereIsNotNull(self, col, conector:str = 'AND'):
        
        return self.whereIsNull(col, conector, type="NOT")
    
    
    def whereLike(self, col:str, value:str, conector:str="AND"):
        
        keyParamValue, keyParam = self.__paramKey(f"like{col}")
        self.__params[keyParamValue] = value
        
        where = f" {col} LIKE {keyParam} " 
            
        self.__conditional.append({"where":where, "conector":conector})    
        return self
    
    def whereBetween(self, col:str, date1:str, date2:str, conector:str="AND"):
               
        keyParamValue, keyParam1 = self.__paramKey(f"like{col}")
        self.__params[keyParamValue] = date1     
        
        keyParamValue, keyParam2 = self.__paramKey(f"like{col}")
        self.__params[keyParamValue] = date1
        
        where = f" {col} BETWEEN {keyParam1} AND {keyParam2} " 
        
        self.__conditional.append({"where":where, "conector":conector})    
        
        return self
       
    # pos condicional   -------------------------------------------------------------         
    
    def limit(self, limit:int):
        self.__limit = limit
        return self
    
    
    def offset(self, offset:int):
        self.__offset = offset
        return self
    
    
    def groupBy(self, group:str|list[str]):  
        
        if type(group) == str:    
            grouped = group
            
        else:            
            grouped = ""
            for gr in group:
                grouped += f"{gr}, "
            grouped = grouped[:-2] 
            
        
        self.__group = grouped
            
        return self
    
    
    def orderBy(self, order:str|list[str]):  
    
        if type(order) == str:    
            ordered = order
            
        else:            
            ordered = ""
            for col, dir in order.items():        
                ordered += f"{col} {dir}, "
            ordered = ordered[:-2] 
            
        
        self.__order = ordered
            
        return self
     
    

    
    
        
    # insert update delete-------------------------------------------------------------
    def insert(self, data:dict|list[dict]):    
        
        self.__construct_insert_query(data)  
        
        query = self.__conn.getQuery(self.__SQL, data)
  
        type_insert = False if type(data) == dict else True
        
        return query.execute_insert(type_insert)    
        
        
    def update(self, data:dict):   
        
        self.__construct_update_query(data)
        return self.__conn.getQuery(self.__SQL,  self.__params).execute_update()    
       

    def delete(self):        
       
        if self.__softDelete == False:
            self.__construct_delete_query()
            return self.__conn.getQuery(self.__SQL,  self.__params).execute_delete()    
        else:   
            now = datetime.now()
            self.__construct_update_query({self.__softDelete:now})
            return self.__conn.getQuery(self.__SQL,  self.__params).execute_update()   
       
       
    def active(self): 
        if self.__withTrashed:
            self.__construct_update_query({self.__softDelete:None})
            return self.__conn.getQuery(self.__SQL,  self.__params).execute_update()   

    



    
    # finalização-------------------------------------------------------------    
    
    def get(self):
        
        self.__construct_select_query() 
        
        result =  self.__conn.getQuery(self.__SQL, self.__params).execute()      
        data = json.dumps(result, default=self.__convert_datetime_to_string)    
        data = json.loads(data) 
                    
        if type(data) == list:
            for row in data:
                cols_to_remove = [col for col in row.keys() if col in self.__not_columns]
                
                for col in cols_to_remove:
                    if col in self.__not_columns:
                        row.pop(col)
        
        return data   
       
    
    def first(self):
        self.__construct_select_query()      
        
        result = self.__conn.getQuery(self.__SQL, self.__params).execute(False) 
        data = json.dumps(result, default=self.__convert_datetime_to_string)    
        data = json.loads(data)    
        
        if type(data) == dict:
            cols_to_remove = [col for col in data.keys() if col in self.__not_columns]
            for col in cols_to_remove:
                if col in self.__not_columns:
                    data.pop(col)
        
        return data

    
    def toSql(self):
        
        if self.__last_method == 'select':              
            self.__construct_select_query()
            
        return self.__SQL
    
    
    def toInfo(self):
        if self.__last_method == 'select':     
            self.__construct_select_query()
            
        return {'conn':self.__conn, 'type':self.__last_method, 'queries':self.__queries, 'params':self.__params}
    
    
    def toParams(self):
        return self.__params
        
    
   
    
    
    
    
    
    
    # misc-------------------------------------------------------------
    
    
    def __construct_select_query(self):    
        
        sql = "SELECT "    
        
        
        #colunas
        tableColAlias = "" if self.__table_alias == None else self.__table_alias + "."
        
        columns = ""
        for col in self.__columns:
            
            if col['name'] not in self.__not_columns:                            
                colAlias = ''
                if 'alias' in col:
                    if col['alias'] != '':
                        colAlias = f" AS {col['alias']}"
            
                columns += f"{tableColAlias}{col['name']}{colAlias}, "             
        columns = columns[:-2]           
        if columns != "":
            sql += columns.strip() +" "
        
        
        
        #alias       
        tableAlias = "" if self.__table_alias == None else self.__table_alias       
        if columns != "":
            sql += " FROM " + self.__table +" "
        else:
            sql += f" FROM {self.__table} {tableAlias}" +" "
        
        
      
        
        
        #condicional
        if self.__softDelete != False:
            if self.__withTrashed == False:
                self.whereIsNull(self.__softDelete)
                
            
        where = ""
        for wheres in self.__conditional: 
            queryWhere = wheres['where']      
            where += f" {wheres['conector']} ({queryWhere})"            
        if where != '' :
            where = f" WHERE {where} "  
        where = where.replace("WHERE  AND","WHERE").replace("WHERE  OR","WHERE")
        where = where.strip()
        if where != "":
            sql += where + " "
        
 
         
         
        #group
        groupby = "" if self.__group == None else f" GROUP BY {self.__group}"
        groupby =  groupby.strip()
        if groupby != "":
            sql += groupby + " "
            
        orderby = "" if self.__order == None else f" ORDER BY {self.__order}"
        orderby =  orderby.strip()
        if orderby != "":
            sql += orderby + " "    
            
        #limit and offset               
        limit = f" LIMIT {self.__limit}" if self.__limit != None else ""
        limit = limit.strip()
        if limit != "":
            sql += limit + " "
        
        offset = f" OFFSET {self.__offset}" if self.__offset != None else ""
        offset = offset.strip()
        if offset != "":
            sql += offset + " "    
            
        
        
        self.__SQL = sql.strip()
        
        self.__queries.append(sql)
    
    
    def __construct_insert_query(self, data):
        self.__last_method = 'insert'         
        
        data = [data] if type(data) == dict else data
        
        for row in data:
            cols = ""         
            values = ""   
            for col, value in row.items():
                keyParamValue, keyParam = self.__paramKey(col, True)               
                
                cols += f"{col}, "
                values += f"{keyParam}, "
                
        cols = cols[:-2]        
        values = values[:-2]     
                
        self.__SQL = f"INSERT INTO {self.__table} ({cols}) VALUES ({values})"    
    
    
    def __construct_update_query(self, data):
        
        self.__last_method = 'update'
        
        values = ""
        for key, value in data.items():
            keyParamValue, keyparam = self.__paramKey(key)
            self.__params[keyParamValue] = value
            
            values += f"{key} = {keyparam}, "  
                         
        values = values[:-2]   
        self.__values_update = values  
        
        
        #condicional
        where = ""
        for wheres in self.__conditional: 
            queryWhere = wheres['where']      
            where += f" {wheres['conector']} ({queryWhere})"            
        if where != '' :
            where = f" WHERE {where} "  
        where = where.replace("WHERE  AND","WHERE").replace("WHERE  OR","WHERE")
        
        self.__SQL = f"UPDATE {self.__table} SET {self.__values_update} {where}"     
    
    
    def __construct_delete_query(self):
        
        self.__last_method = 'delete'
        
        #condicional
        where = ""
        for wheres in self.__conditional: 
            queryWhere = wheres['where']      
            where += f" {wheres['conector']} ({queryWhere})"            
        if where != '' :
            where = f" WHERE {where} "  
        where = where.replace("WHERE  AND","WHERE").replace("WHERE  OR","WHERE")
        
        self.__SQL = f"DELETE FROM {self.__table} {where}"     
                  
    
    def __lenParams(self):
        return len(self.__params)
    
    
    def __paramKey(self, key, insert = False):
        pIndex = self.__lenParams()
        
        if insert == False:
            keyparam = f"{self.__table}_{key}_{pIndex}".replace('.',"_")
        else:
            keyparam = key

        return f"{keyparam}", f"%({keyparam})s"
    
    
    def upColumns(self, data):
        self.__columns = self.__columns + (data)
        
        
    def __convert_datetime_to_string(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        raise TypeError("Tipo de objeto não serializável")        