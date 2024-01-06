import os, glob, importlib
from pathlib import Path
from KassOrm._helpers import getStub
from datetime import datetime as dt
from KassOrm.Querier import Querier
from KassOrm.Conn import Conn


class Migration:
    __file__ = None
    __conn__ = None
    __type__ = None
    __table__ = None
    __comment__ = None

    __rollback__ = False

    def __init__(self) -> None:
        self.__sql = ""

        self.__params = {}

        self.__columns = []

        self.__column = {}

        self.__primary_key = None
        
        self.__rollback = False
        
        self.__add_column = []


    def make_file_migration(self, name_migration, dir_migrations, table, comment: str = ""):
        """Responsável por criar os arquivos de migração"""
        name_migration = name_migration.lower()
        
        dir_migrations = Path(dir_migrations)

        if os.path.isdir(dir_migrations) == False:
            os.makedirs(dir_migrations)

        if "create" in name_migration:
            content = getStub("migration_create.stub")
        else:
            content = getStub("migration_alter.stub")

        content = content.replace(
            "%COMMENT%", f"'{comment.lower()}'" if comment != "" else "''"
        )
        content = content.replace("%TABLE%", table)

        filename = dt.now().strftime("%Y_%m_%d__%H%M%S") + "_" + name_migration + ".py"
        file = open(f"{dir_migrations}/{filename}", "w+", encoding="utf-8")
        file.writelines(content)
        file.close()


    def generate_query_create(self):
        """Gera uma query de criação de tabela"""
        self.__sql = "CREATE TABLE IF NOT EXISTS {} (".format(self.__table__)

        for col in self.__columns:
            column = ""
            for value in col.values():
                column += f"{value} "

            self.__sql += f"{column}, "

        if self.__primary_key != None:
            self.__sql += "PRIMARY KEY ({}), ".format(self.__primary_key)

        self.__sql = self.__sql[:-2]
        self.__sql += ");"
        
       
       
    def generate_query_alter(self):
        """Gera uma query de alteração de tabela"""
        
        self.__sql = "ALTER TABLE {} ".format(self.__table__)

        for col in self.__columns:
            column = ""
            for value in col.values():
                column += f"{value} "

            self.__sql += f"{column}, "


        self.__sql = self.__sql[:-2]
        


    def generate_query_rollback(self):
        """Gera uma query de alteração, drop ou exclusão de tabela"""
        
        pass 



    def generate_query(self):
        """Gerencia qual query gerar"""
        
        
        # up e down configura as colunas e o q for para gerar a query
        if self.__rollback == False:
            self.up()
        else:
            self.down()
            
            
        # gera a query de acordo com as configs de up ou down
        if self.__type__ == "create" and self.__rollback == False:
           self.generate_query_create()

        elif self.__type__ == "alter": 
            self.generate_query_alter()


    def setRollback(self):
        self.__rollback = True
        return self


    def execute(self):
        """Principal método de execução da migration, gera o sql do arquivo migration e o executa"""
 
        try:
            self.generate_query()  
            
            result = Conn().getQuery(self.__sql, self.__params).execute_create()
            return result
        except Exception as err:
            print("execute: " + str(err))
            return False


    def execute_migrate(self, module_name:str):
        """Executa o metodo execute da classe migrate do arquivo migration""" 
        module = importlib.import_module(module_name)
        return module.migrate(), module.migrate().execute()
    
    
    def execute_rollback(self, module_name:str):
        module = importlib.import_module(module_name)
        return module.migrate(), module.migrate().setRollback().execute()
    
    
    def catch_module_and_migrations(self, dir_migrations):
        """Retorna o nome do diretório como módulo e todas as migrações do diretorio"""
        migrations = glob.glob(os.path.join(dir_migrations, "*.py"))
        dir_module = str(dir_migrations).replace("\\", ".")
        return dir_module, migrations


    def has_migration_executed(self, migration:str):
        """Verifica se a migração foi executada, salva na tabela _migrations_"""
        try:
            return Querier().table("_migrations_").where({"migration":migration}).first()
        except Exception as err:
            print(str(err))
            return False
     
     
    def save_migration_executed(self, migration: str, description: str = None):
        """Salva registro da migração executada na tabela _migrations_"""
        try:
            # sql = """INSERT INTO _migrations_ (date, migration, description) VALUES (NOW(), %(migration)s, %(description)s)"""
            # Conn().getQuery(
            #     sql, {"migration": migration, "description": description}
            # ).execute_insert()

            now = dt.now() 
            Querier().table('_migrations_').insert({"date":now,"migration":migration,"description":description})
            return True
        except Exception as err:
            print("save_migration_executed:"  +str(err))
            return False
    
    
    def delete_migration_executed(self, id):
        
        Querier().table('_migrations_').where({"id":id}).delete()
        return True


    def execute_all_migrations(self, dir_migrations: str):
        """Executa todas as migrações do diretorio informado"""

        dir_module, migrations = self.catch_module_and_migrations(dir_migrations)
            
        step = 1
        for migration in migrations:
            file = os.path.basename(migration).replace(".py", "")  
            
            
            if self.has_migration_executed(file) == 'null':       
                module, result = self.execute_migrate(f"{dir_module}.{file}")

                if result == True:
                    self.save_migration_executed(file, module.__comment__)
                    print(f"{file} {self.color('green')}[OK]{self.color()}")
                else:
                    print(f"{file} {self.color('red')}[Fail]{self.color()}")
                    
                    self.rollback(dir_migrations, step)
                    return False

            else:
                print(f"{file} {self.color('yellow')}[ALREADY EXISTS]{self.color()}")

            step +=1

        
        return True


    def drop_all_migrations(self, dir_migrations: str):
        migrations = glob.glob(os.path.join(dir_migrations, "*.py"))

        self.drop_table_migrations()

        dir_module = str(dir_migrations).replace("\\", ".")

        for migration in migrations:
            file = os.path.basename(migration).replace(".py", "")
            
            module, result = self.execute_rollback(f"{dir_module}.{file}")            

            print(f"{file} {self.color('yellow')} [DROPPED]" + self.color())
            
        return True
















    def up(self):
        return self

    def down(self):
        return self

    #  TIPOSS ------------------

    def add(self):
        self.__columns.append(self.__column)
        self.__column = {}
        return

    def id(self):
        self.__column["name"] = "id"
        self.__column["type"] = "BIGINT"
        self.__column["unsigned"] = "UNSIGNED"
        self.__column["isNull"] = "NOT NULL"
        self.__column["autoIncrement"] = "AUTO_INCREMENT"
        self.__column["primary_key"] = "PRIMARY KEY"
        
        

        return self

    def string(self, name, qnt: int = 255):
        self.__column["name"] = name
        self.__column["type"] = f"VARCHAR({qnt})"
        self.__column["isNull"] = "NOT NULL"

        return self

    def bigInteger(self, name):
        self.__column["name"] = name
        self.__column["type"] = f"BIGINT"
        self.__column["isNull"] = "NOT NULL"

        return self

    def bigIntegerUnisigned(self, name):
        self.__column["name"] = name
        self.__column["type"] = f"BIGINT UNSIGNED"
        self.__column["isNull"] = "NOT NULL"

        return self

    def text(self, name):
        self.__column["name"] = name
        self.__column["type"] = f"TEXT"
        self.__column["isNull"] = "NOT NULL"

        return self

    def enum(self, name: str, values: list):
        str_values = ", ".join(map(lambda x: f'"{x}"', values))

        self.__column["name"] = name
        self.__column["type"] = f"ENUM({str_values})"
        self.__column["isNull"] = "NOT NULL"

        return self

    def integer(self, name: str, qnt: int = None):
        self.__column["name"] = name

        if qnt != None:
            self.__column["type"] = f"INT({qnt}) ZEROFILL UNSIGNED"
        else:
            self.__column["type"] = f"INT"
        self.__column["isNull"] = "NOT NULL"

        return self

    def datetime(self, name: str):
        self.__column["name"] = name
        self.__column["type"] = "DATETIME"
        self.__column["isNull"] = "NOT NULL"

        return self

    def nullable(self):
        self.__column["isNull"] = "NULL"

        return self

    def unsigned(self):
        self.__column["unsigned"] = "UNSIGNED"

        return self

    def comment(self, comment: str):
        self.__column["comment"] = f"COMMENT '{comment}' "
        return self

    def unique(self, columns: list = None, name=None):
        if columns != None or name != None:
            uniq = ""
            for col in columns:
                uniq += f"{col}, "

            uniq = uniq[:-2]

            self.__column["unique_key"] = f" UNIQUE KEY {name} ()"
            return self
        else:
            self.__column["unique"] = f"UNIQUE"
            return self

    def current_timestamp(self):
        self.__column["current_timestamp"] = "DEFAULT CURRENT_TIMESTAMP"

        return self

    def update_timestamp(self):
        self.__column["on_update_timestamp"] = "ON UPDATE CURRENT_TIMESTAMP"

        return self

    # TOOLS-----------

    def addColumn(self):
        self.__column["add"] = "ADD COLUMN "

        return self

    def dropColumn(self, name):
        self.__column["drop"] = "DROP COLUMN {} ".format(name)
        return self

    def after(self, column: string):
        self.__column["after"] = f"AFTER {column}"
        return self

    def first(self, column: string):
        self.__column["first"] = f"FIRST {column}"
        return self

    def dropTableIfExists(self):
        self.__sql = "DROP TABLE IF EXISTS {}".format(self.__table__)

    def color(self, code=""):
        """Cores para usar no terminal"""

        if code == "green":
            return "\033[0;32m"

        elif code == "yellow":
            return "\033[0;33m"

        elif code == "red":
            return "\033[0;31m"

        else:
            return "\033[m"

    def create_table_migrations(self):
        try:
            sql = """
                CREATE table if not exists _migrations_ (
                id BIGINT unsigned not null auto_increment,
                date DATETIME not null,
                migration VARCHAR(255) not null unique,
                description VARCHAR(255) null,
                PRIMARY KEY (`id`)
                );
            """
            Conn().getQuery(sql, {}).execute_create()
            return True
        except Exception as err:
            print("create_table_migrations: "+str(err))
            return False

    def drop_table_migrations(self):
        try:
            sql = "DROP TABLE IF EXISTS _migrations_"
            Conn(None).getQuery(sql, None).execute_create()
            return True
        except Exception as err:
            print("drop_table_migrationsstr: "+(err))
            return False

 

  

    def migrate(self, dir_migrations):
        
        dir_migrations = Path(dir_migrations)
        hasCreated = self.create_table_migrations()

        if hasCreated==False:
            return False
        
        result = self.execute_all_migrations(dir_migrations)

        return  result




    def rollback(self, dir_migrations, steps):
       
       dir_migrations = Path(dir_migrations) 
        
       migrations = Querier().table('_migrations_').orderBy("id DESC").limit(steps).get()
       
       dir_module = str(dir_migrations).replace("\\", ".")
        
       for migration in migrations:
            file = migration['migration']            

            module, result = self.execute_rollback(f"{dir_module}.{file}")
            
            if result == False:
                print(result)
                return False
            
            self.delete_migration_executed(migration['id'] )


       
       return True