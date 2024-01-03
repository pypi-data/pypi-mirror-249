

def getStub(name):      
    stub = open(f"KassOrm/stubs/{name}",'r+')
    stub_content = stub.read()
    stub.close()    
    
    return stub_content