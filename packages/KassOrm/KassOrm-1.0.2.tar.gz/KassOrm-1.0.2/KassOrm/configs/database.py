import os
from dotenv import dotenv_values

"""
Conexões existentes
Configure aqui seus bnaco de dados

Drivers aceitos: Mysql
"""
connections = {
    
    "default": {
        # "driver": os.getenv("DB_DRIVER","mysql"),
        "user": os.getenv("DB_USER","root"),
        "password": os.getenv("DB_PASSWORD",""),
        "host": os.getenv("DB_HOST","127.0.0.1"),
        "port": os.getenv("DB_PORT",3306),
        "database": os.getenv("DB_DATABASE",""),
        
        
        #POOL CONFIG
        # "pool_name": "ormkass_pool",
        # "pool_size": 5,
        # "pool_reset_session": True,
        # "connect_timeout": 30,
    },
    
}



"""
Define quais conexões  em 'connections' usam softDelete
Informe o nome da conexão e qual o campo padrão para determinar a exclusão

Padrão: default => deleted_at
"""
useSofdelete = {    
    "default": os.getenv("SOFTDELETE_DEFAULT","deleted_at"),
}






