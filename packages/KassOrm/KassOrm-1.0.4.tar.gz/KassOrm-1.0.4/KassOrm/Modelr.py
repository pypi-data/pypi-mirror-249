from .Querier import Querier
import json
from pathlib import Path
import os
from KassOrm._helpers import getStub

class Modelr():
    
     
    __sofDelete__ = False   
    __table__ = None   
    __conn__ = None    
    
    
    def __init__(self) -> None:  

        self.query = Querier(conn=self.__conn__, softDelete=self.__sofDelete__).table(self.__table__)      
        
        self.__has = []      
        
        self.__queries = []     
    
    
    # get data -----------------------------------------------------------
      
    
    def first(self):        
        return self.execute('first')
    
    
    def get(self):   
        return self.execute('get')
    

    def execute(self, type:str):    
        
        if type == 'get':  
            data = self.query.get() 
            data = self.check_relationships(data)  
            
        elif type == 'first':       
            data = self.query.first()           
            data = self.check_relationships(data, True)  
            
        elif type == 'onlysql':
            self.__queries.insert(0,{"query":self.query.toSql(),"params":self.query.toParams()})
            data = self.query.get()   
            
            if data != None:
                self.check_relationships(data, False, True) 
            return            
  
       
       
        return data 
      
      
    # get info -----------------------------------------------------------
    
    
    def toSql(self):        
        query = self.query.toSql()
  
        for key, value in  self.query.toParams().items():              
            query = query.replace(f"%({key})s",str(value))
                              
        return query            
    
    
    def toSqls(self):
        return self.getInfo(True)
    
    
    def toInfo(self):        
        return {"query":self.query.toSql(), "params":self.query.toParams()}
    
    
    def toInfos(self):
        return self.getInfo()
 
    
    def getInfo(self, binded = False):      
        self.execute('onlysql')
        
        if binded:
            queries = []
            for x in self.__queries:
                query = x['query']
                for key, value in x['params'].items():              
                    query = query.replace(f"%({key})s",str(value))
                
                queries.append(query)
                    
            return queries                    
                   
        else:
            return self.__queries
         
         
             
    
    # select ------------------------------------------------
        
    def select(self, columns:list):
        self.query.select(columns)
        return self
    
    def notSelect(self, columns:list):
        self.query.notSelect(columns)
        return self
    
    
    
    # insert ---------------------------------------------------------

    def insert(self, data:dict|list[dict]):
        return self.query.insert(data)
    
    
    # update -------------------------------
    def update(self, data):
        return self.query.update(data)
    
    
    # delete ------------------------------------------------------------
    
    def delete(self):
        return self.query.delete()
        
        
    def active(self):
        return self.query.active()
    
    
    def withTrashed(self):
        self.query.withTrashed()
        return self
    
    
    
    
    # condicional-----------------------------------------------------------    
    
    def where(self, values:dict, conector:str = 'AND' ):
        self.query.where(values, conector)
        return self
        
    def whereIn(self, column:str, values:list, conector:str = 'AND', type:str = ''):
        self.query.whereIn(column, values, conector, type)
        return self
        
    def whereNotIn(self, column:str, values:list, conector:str = 'AND'):
        self.query.whereNotIn(column, values, conector)
        return self
    
    def orWhere(self, values:dict):
        self.query.orWhere(values)
        return self
    
    def whereIsNull(self, column:str, conector:str = 'AND', type:str = ''):
        self.query.whereIsNull(column, conector , type)
        return self
    
    def whereIsNotNull(self, column:str,  conector:str = 'AND'):
        self.query.whereIsNotNull(column, conector)
        return self
    
    def whereLike(self, column:str, values:list, conector:str = 'AND'):
        self.query.whereLike(column, values, conector)
        return self
    
    
    
    # pos condicional -----------------------------------
    
    def limit(self, limit:int):
        self.query.limit(limit)
        return self
    
    
    def offset(self, offset:int):
        self.query.offset(offset)
        return self
    
    
    def groupBy(self, group:str|list[str]):  
        self.query.groupBy(group)            
        return self
    
    
    def orderBy(self, order:str|list[str]):  
        self.query.orderBy(order)            
        return self
     
    

    
    
    
    # relashionship -----------------------------------------------------------
    
    
    def has(self, model:str, model_key:str, intermediate_model_key:str=None, intermediate_table:str=None, intermediate_local_key:str=None, local_key:str=None, type:str=None):
        table_local = self.__table__        
        table_model = model.__table__             
        
        for related in self.__has:
            for a in related.values():
                check = len(a)
                if check == 0:
                    key = list(related)[0]
                    related[key] = {
                        "type":type,                         
                        "local_table":table_local, 
                        "local_key":local_key, 
                        "intermediate_table":intermediate_table,
                        "model_table":table_model,
                        "model_key":model_key,     
                        "intermediate_model_key":intermediate_model_key,
                        "intermediate_table":intermediate_table,
                        "intermediate_local_key":intermediate_local_key                        
                        }
                                
    
    def hasOne(self, model, model_key, local_key): 
        self.has( 
                 model=model,
                 model_key=model_key,
                 local_key=local_key,
                 type='one'
                )
                    
       
    def hasMany(self, model, model_key, local_key):
        self.has(
                model=model,
                 model_key=model_key,
                 local_key=local_key,
                 type='many'
                 )
       
       
    def hasManyToMany(self, model, model_key, intermediate_model_key , intermediate_table, intermediate_local_key, local_key):
        self.has(
                model=model,
                model_key=model_key, 
                intermediate_model_key=intermediate_model_key,
                intermediate_table=intermediate_table,
                intermediate_local_key=intermediate_local_key,
                local_key=local_key,
                type='manytomany'
                ) 
        self.selected_related = model.__table__
        return self         
      
      
    def withPivot(self, columns:list[str]|bool = True):    
        
        for related in self.__has:
            for key in related.keys():                
                if self.selected_related == key:           
                    related[key]['pivot'] = columns
            
           
    def related(self, model:list|str):   
        
        def x(d):               
            method = getattr(self, d)       
            self.__has.append({method.__name__:{}})             
            method()  
            
        
        if type(model) == str:
            x(model)
        else:
            for i in model:
                x(i)
                
        return self
    
            
    def check_relationships(self, data, first = False, onlySql = False):                 
        
        data_json = data if type(data) == list else data          
        data_json = data_json if type(data_json) == list else [data_json]  
        
        
        for dictr in self.__has:  
            for rel, value in dictr.items():        
                if value['type'] in ['many','one']:              
                    data_json = self.check_relationships_one_many(rel, value, data_json, onlySql)               
            
                elif value['type'] in ['manytomany']:                    
                    data_json = self.check_relationships_manytomany(rel, value, data_json, onlySql)
                        
   
        if onlySql==False:   
            return data_json[0] if first == True else data_json
        
      
    def check_relationships_one_many(self, rel, value, data_json, onlySql):                   
                    
        all = True if value['type'] == 'many' else False                

        keys = list(set(row[value['local_key']] for row in data_json))
            
        query_related = Querier(self.__conn__).table(value['model_table']).whereIn(value['model_key'], keys)                
        self.__queries.append({"query":query_related.toSql(),"params":query_related.toParams()})            
            
        if onlySql==False:    
            data_rel = query_related.get()                      
            if all:   
                for row in data_json:           
                    row[rel] = None                                       
                    for relrow in data_rel:        
                        if row[value['local_key']] == relrow[value['model_key']]:
                            if row[rel] == None:                                                           
                                row[rel] = []                                        
                            row[rel].append(relrow)    

                                
            else:
                for row in data_json:   
                    for relrow in data_rel: 
                        if row[value['local_key']] == relrow[value['model_key']]:
                            if rel not in row.keys():                                
                                row[rel] = relrow
                            else:      
                                row[rel] == None
                                        
        return data_json                                            
                                        
    
    def check_relationships_manytomany(self, rel, value, data_json, onlySql):
        local_keys = list(set(row[value['local_key']] for row in data_json))
   
        #acessar intermediaria
        query_intermediated = Querier(self.__conn__).table(value['intermediate_table']).whereIn(value['intermediate_local_key'], local_keys)                
        self.__queries.append({"query":query_intermediated.toSql(),"params":query_intermediated.toParams()}) 
        
   
        #resgatar ids do modelo relacionado   
        data_intermediate_json = query_intermediated.get()
        # data_intermediate_json = json.loads(data_intermediate_json)           
        data_intermediate_json = data_intermediate_json if type(data_intermediate_json) == list else [data_intermediate_json]
        intemediate_model_keys = list(set(row[value['intermediate_model_key']] for row in data_intermediate_json))

            
        if intemediate_model_keys != []:
            #acessar table do model   
            query_model = Querier(self.__conn__).table(value['model_table']).whereIn(value['model_key'], intemediate_model_keys)                
            self.__queries.append({"query":query_model.toSql(),"params":query_model.toParams()})    
            data_rel = query_model.get()
        else:
            data_rel = []         
   
        
        
        #mesclando relacionamentos
        # data_rel = json.loads(query_model.get()) 
        local_counter = 0
        for local_row in data_json:          
            local_counter +=1
            
            if rel not in local_row:  
                local_row[rel] = None 
            
            inter_counter = 0            
            for interdata_row in data_intermediate_json:  
                inter_counter +=1
                
                # if rel not in local_row:  
                #     local_row[rel] = None 
                              
                model_counter = 0           
                for model_row in data_rel: 
                    model_counter +=1                   

                     
                    if local_row[value['local_key']] == interdata_row[value['intermediate_local_key']] and\
                       model_row[value['model_key']] == interdata_row[value['intermediate_model_key']]:  
                           
                        if "pivot" in value:
                            if type(value['pivot']) == list:
                                model_row['pivot'] = {col: interdata_row[col] for col in interdata_row if col in value['pivot'] and interdata_row[value['intermediate_model_key']] == model_row[value['model_key']] }
                            else:  
                                model_row['pivot'] = interdata_row 
                            
                        if local_row[rel] == None:  
                            local_row[rel] = [] 
                            
                        local_row[rel].append(model_row)                                 
                
        
        return data_json
    
    
    
    
    def make_file_model(self, dir_models, table, comment: str = ""):
        """Responsável por criar os arquivos de modelos"""
        # table = table.
        
        dir_models = Path(dir_models)
        # modelname = table.replace("_"," ").capitalize().replace(" ","")
        
        parts = table.split('_')
        modelname = parts[0] + ''.join(x.title() for x in parts[1:])
        modelname = modelname.capitalize()
        filename = modelname + ".py"

        if os.path.isdir(dir_models) == False:
            os.makedirs(dir_models)
            
        if os.path.isfile(f"{dir_models}/{filename}") == True:            
            return f'{modelname} - Model already created'
        
        content = getStub("model.stub")


        content = content.replace("%COMMENT%", f"'{comment.lower()}'" if comment != "" else "''")
        content = content.replace("%TABLE%", table)
        content = content.replace("%MODELNAME%", modelname)
        

        
        file = open(f"{dir_models}/{filename}", "w+", encoding="utf-8")
        file.writelines(content)
        file.close()
        
        return True