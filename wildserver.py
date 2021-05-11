from utils import *
from DataBase import *
from distutils.dir_util import copy_tree
import shutil
import subprocess
paths = load_json_file("paths.json")
#print(paths)
def start_server():
    dir_src = paths['WILDFLY_DEPLOYMENTS']
    wildpath = paths['WILDFLY_BIN']
    print ("Wildfly started successfully")
    #url = 'http://localhost:8080/'+project_name
    if isLinux():
        #subprocess.Popen(["bash",f"{wildpath}/standalone.sh"])
        #subprocess.check_output(["bash",f"{wildpath}/standalone.sh"])
        print()
        os.system(f"bash {wildpath}/standalone.sh")
        #webbrowser.open(url)
    else:    
        #webbrowser.register('chrome', None,webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
        #webbrowser.get('chrome').open(url)
        os.system(f'{wildpath}/standalone.bat')






def restart_server():
    wildpath = paths['WILDFLY_BIN']
    #os.chdir(paths['WILDFLY_BIN'])
    #print(os.getcwd())
    if isLinux():
        os.system(f'{wildpath}/./jboss-cli.sh --connect command=:reload')
    else:
        os.system(f'{wildpath}/jboss-cli.bat --connect command=:reload')
    print ("wildfly restarted successfully")

   
def navigate_and_renamejson(src,project_name):
    new_json=project_name+'.json'
    for item in os.listdir(src):
        s = os.path.join(src, item)      
        if s.endswith(".json"):
            shutil.copy(s, os.path.join(src, new_json))
    with open(new_json, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('ecommerce', project_name)
    with open(new_json, 'w') as file:
        file.write(filedata)
 
def navigate_and_renameds(src,project_name):
    new_ds=project_name+'-ds.xml'
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if s.endswith("-ds.xml"):
            shutil.copy(s, os.path.join(src, new_ds))
    with open(new_ds, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('ecommerce', project_name)
    with open(new_ds, 'w') as file:
        file.write(filedata)





def TurnOn(project,can_restart=True):
    project_name=project+'.war'
    project_json=project+'.json'
    project_ds=project+'-ds.xml'
    src_path=paths['UPLOADS_FOLDER']+"/"+project_name
    src_json=paths['UPLOADS_FOLDER']+"/"+project_json
    src_ds=paths['UPLOADS_FOLDER']+"/"+project_ds
    d_path=paths['WILDFLY_DEPLOYMENTS']
    # del_path="C:/Users/Dell/wildfly-20.0.0.Final/standalone/deployments/"+project_name
    del_path=paths['WILDFLY_DEPLOYMENTS']+project_name
    del_json=d_path+project_json
    del_ds=d_path+project_ds
    copy_tree(src_path, d_path+project_name)
    shutil.copy(src_json,d_path)
    shutil.copy(src_ds,d_path)
    print("Copied")
    if can_restart:
        restart_server()   

def TurnOff(project_name):
    project_name=project_name+'.war'
    project_json=project_name+'.json'
    project_ds=project_name+'-ds.xml'
    d_path=paths['WILDFLY_DEPLOYMENTS']
    # del_path="C:/Users/Dell/wildfly-20.0.0.Final/standalone/deployments/"+project_name
    del_path=paths['WILDFLY_DEPLOYMENTS']+project_name
    del_json=d_path+project_json
    del_ds=d_path+project_ds
    print(del_path)
    shutil.rmtree(del_path,ignore_errors=True)
    os.remove(del_ds)
    os.remove(del_json)    
    #os.getcwd()
    restart_server() 


def start_all_projects():
    project_list = Project.query.all()
    #for project in project_list:
    #    TurnOn(project.project_name,False)
    start_server()