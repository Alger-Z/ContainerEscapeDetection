

def _init():
    global global_dict
    global_dict={}
    #map new syscall type to old 
    global_dict["sc_n2o"]={ 
        "select":"pselect6",
        "pipe":"pipe2",
        "access":"faccessat",
        "newfstatat":"fstatat",
        "lstat":"fstatat",
        "open_by_handle_at":"openat",
        "stat":"fstatat",
        "mkdir":"mkdirat",
        "readlink":"readlinkat",
        "getdents":"getdents64",
        "dup2":"dup",
        "chown":"fchown",
        "getpgrp":"getpgid",
        "arch_prctl":"prctl"
    }
    #sequence size for syscall number txt 
    global_dict["seq_size"] =10000
    global_dict["debug"]=False
    global_dict["sc_map_json"] ="sc_map.json"
    
    global_dict["dir_mysql_train"] = "data/mix_txt"
    global_dict["dir_mysql_test"] = "data/mysqltxt_test"
    global_dict["dir_dvwa_train"] ="data/dvwatxt"
    global_dict["dir_dvwa_test"] = "data/dvwatxt_test"
    global_dict["dir_escp"]="data/att_withreq"
    
    global_dict["logpath"]  = "data/dvwa/dvwa-test/log/"
    global_dict["txt_path"] ='data/dvwatxt/'

    global_dict["mysql_log_path"]= "data/mysql/mix_big"
    global_dict["mysql_txt_path"]="data/mysqltxt/mix/"
    
    
def set_debug():
    global_dict["debug"] =True
    return global_dict["debug"]
def get_debug():
    return global_dict["debug"]
def get_array_limit():
    if global_dict["debug"] :
        arraysize = 2000
        arraycount=2 
    else :
        arraysize = 100000
        arraycount= 10
    return arraysize,arraycount
def get_data_dir(name):
    return global_dict[name]
def get_seq_limit():
    return global_dict["seq_size"]