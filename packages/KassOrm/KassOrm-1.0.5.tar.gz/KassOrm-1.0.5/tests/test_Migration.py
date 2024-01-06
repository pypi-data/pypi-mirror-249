from pathlib import Path
import os,shutil
import pytest
from KassOrm.Migration import Migration  
import pdb
import time


_PATH_ = Path("_tests_results_/tests_migrations")

@pytest.fixture
def reset_migration_tests():
    dir_migration = Path(f"{_PATH_}/api/database")  
    
    Migration().drop_all_migrations(dir_migration)
    
    
    if os.path.isdir(_PATH_) == True:
        shutil.rmtree(_PATH_)
    os.makedirs(f"{_PATH_}")  
    
    
def test_create_file_migration(reset_migration_tests):       
    name_migration = "create_users" 
    dir_migration = f"{_PATH_}/api/database"
    comment = "Criação da tabela de usuários"
    table = 'users'    
    
    time.sleep(1)
    Migration().make_file_migration(name_migration, dir_migration, table, comment)
    
    assert os.path.isdir(dir_migration), f"Migration {name_migration} not created!"
    
    
# Alterar stub migration_alter.stub para funcionar     
# def test_alter_file_migration():
#     name_migration = "alter_users" 
#     dir_migration = f"{_PATH_}/api/database"
#     comment = "Criação do campo nome em users"
#     table = 'users'
    
#     time.sleep(1)    
#     Migration().make_file_migration(name_migration, dir_migration, table, comment)
    
#     assert os.path.isdir(dir_migration), f"Migration {name_migration} not created!"
    
    
def test_execute_migrations():    
    
    dir_migration = f"{_PATH_}/api/database"      
    
    result = Migration().migrate(dir_migration)
    print(result)
    
    assert result, "Migration not executed!"
    
    
# def test_rollback_one_step():
#     dir_migration = f"{_PATH_}/api/database"
        
#     result = Migration().rollback(dir_migration, 1)   
    
#     assert result, "Migration not excluded!"
    