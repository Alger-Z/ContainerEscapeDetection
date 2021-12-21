

def _init():
    global global_dict
    global_dict={}
    global_dict["debug"]=False

def set_debug():
    global_dict["debug"] =True
    return global_dict["debug"]
def get_debug():
    return global_dict["debug"]