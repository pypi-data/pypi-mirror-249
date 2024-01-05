from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
import threading as th
import pandas as pd 
import json,requests,os,base64

def get_key(auth, key):
    host = os.getenv("API_HOST")
    try:
        res = requests.get(host + "/getkey/" + key, headers=auth,verify=False)
        jsdata = json.loads(res.content.decode("utf-8"))['settingValue']
        return jsdata
    except Exception as e:
        print('!exception!')
        print(e)
        return ""
    
def get_auth():
    creds = {
        "Username": os.getenv("API_UN"),
        "Password": os.getenv("API_PWD"),
        "Role": os.getenv("API_ROLE")
    }
    host = os.getenv("API_HOST")
    login = requests.post(host + "/login", json=creds,verify=False)
    token = login.json()["accessToken"]
    headers = {
        'Authorization': 'Bearer ' + token
    }
    print('auth - done')
    return headers

def test_auth():
    creds = {
        "Username": os.getenv("API_UN"),
        "Password": os.getenv("API_PWD"),
        "Role": os.getenv("API_ROLE")
    }
    print(creds)
    host = os.getenv("API_HOST")
    login = requests.post(host + "/login", json=creds,verify=False)
    print(str(login.status_code))
    token = login.json()["accessToken"]
    print(token)
    headers = {
        'Authorization': 'Bearer ' + token
    }
    print(headers)
    print(host)
    test = requests.get(host + "/test", headers=headers,verify=False)
    print(str(test.status_code))
    print(test.content.decode("utf-8"))

def setup_s21(keys,trusted):
    s21 = Srv21()
    s21.auth = get_auth()
    s21.results = {}
    s21.threads = [] 
    #keys = ['SRV21','DB21']
    
    for k in keys:
        s21.create_thread(k)

    for thread in s21.threads:
        thread.start()
    for thread in s21.threads:
        thread.join()  

    if(trusted):
        s21.conn = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={s21.results[keys[0]]};"
            f"DATABASE={s21.results[keys[1]]};"
            # f"UID={self.USER21};"
            # f"PWD={self.PASS21};"
            f"Trusted_Connection=yes;"
        )
    else:
        s21.conn = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={s21.results[keys[0]]};"
            f"DATABASE={s21.results[keys[1]]};"
            f"UID={s21.results[keys[2]]};"
            f"PWD={s21.results[keys[3]]};"
        )

    #save s21 to a dict
    s21.threads = []
    s21.engine = None
    s21_dict = s21.__dict__

    #s21_dict to base64 string
    s21_json = json.dumps(s21_dict)
    s21_b64 = s21_json.encode('ascii')
    s21_b64 = base64.b64encode(s21_b64)
    #to file
    with open('s21_b64.txt','wb') as f:
        f.write(s21_b64)

def load_s21():
    with open('s21_b64.txt','rb') as f:
        s21_b64 = f.read()
    s21_b64 = base64.b64decode(s21_b64)
    s21_json = s21_b64.decode('ascii')
    s21_dict = json.loads(s21_json)
    s21 = Srv21()
    s21.__dict__ = s21_dict
    s21.set_engine(s21.conn)
    return s21

def first_run(keys,trusted):
    if os.path.isfile('s21_b64.txt'):
        s21 = load_s21()
        return s21
    else:
        setup_s21(keys,trusted)
        s21 = load_s21()
        return s21
    
def query_to_df(session,query):
    df = pd.DataFrame(session.execute(text(query)).fetchall())
    return df

def update_sql(session,query):
    q = text(query)
    session.execute(q)
    session.commit()
    return True
    

class Srv21():
    SRV21:str
    DB21:str
    USER21:str
    PASS21:str
    auth:dict
    results:dict
    threads:list
    engine:any
    conn:str

    def set_conn(self,conn):
        self.conn = conn
        self.results['conn'] = conn

    def get_setting_body(self,name,desc,value,type):
        body = {
            "SettingName": name,
            "SettingDesc": desc,
            "SettingValue": value,
            "SettingType": type
        }
        return body
    
    def create_setting(self,body):
        host = os.getenv("API_HOST")
        create = requests.post(host + "/createkey",headers=self.auth,json=body)
        print(str(create.status_code))
        print(create.content.decode("utf-8"))

    def set_engine(self,conn):
        self.results['conn'] = conn
        self.conn = conn
        self.engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(conn))
        return self.engine
    
    def get_cred(self,cred):
        self.results[cred] = get_key(self.auth,cred)
        return self.results[cred]

    def create_thread(self,cred):
        thread = th.Thread(target=self.get_cred, args=(cred,))
        self.threads.append(thread)
    
    def get_new_session(self):
        return Session(self.engine)