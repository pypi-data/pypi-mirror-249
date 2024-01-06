from pathlib import Path
import os

def getStub(name):   
    
    dir = os.path.dirname(__file__)
    
    stub = open(Path(f"{dir}/stubs/{name}") ,'r+')
    stub_content = stub.read()
    stub.close()    
    
    return stub_content