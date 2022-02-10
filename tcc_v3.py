import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import pandas as pd
import requests, json
from datetime import datetime, date
from matplotlib import style

plt.style.use("seaborn-dark")

for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey

for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey

plt.rcParams['axes.linewidth'] = 0.5
colors = [
    '#08F7FE',  # teal/cyan
    '#f7536a',  # vermelho
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    '#a9fde8',  # g
    '#befda9',  # g
    '#e8a9fd',  # g
    '#fda9be',  # g
    '#f78e53'   # g
]

def run_request(method, url, param=""): 
    if method == "POST":
        request = requests.post(url, json=param)
        response = json.loads(request.text)
        return response

    if method == "GET":
        request = requests.get(url, json=param)
        return request.status_code

def login(cpf_email, senha):
    method = "GET"
    url_login = "http://terguinator.pythonanywhere.com/api/v1/customer/login"
    if "@" in cpf_email == "": param_login = {"email": cpf_email, "senha": senha}
    else: param_login = {"cpf": cpf_email, "senha": senha}

    verifica_login = run_request(method, url_login, param_login)

    if verifica_login == 200: return True
    else: return False

def info_user(cpf):
    method = "GET"
    url = f"http://terguinator.pythonanywhere.com/api/v1/customer/{cpf}/info"
    request = requests.get(url)
    try:
        response = json.loads(request.text)
        return (response["customer"])
    except: print("Something went wrong")

def details(startdate, enddate, tipo, cpf="", estado="", cidade="", bairro=""):
    method = "POST"
    
    if tipo == "customer":     
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/details/query/customer"
        
        if cpf == "1234": param = {"startdate": f"{startdate}", "enddate": f"{enddate}"}  # usuario enel
        else: param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "cpf": f"{cpf}"}    
        pede_valores = run_request(method, url, param)
                
        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo"] = pd.to_numeric(df["consumo"], downcast="float")
        df["anterior"] = pd.to_numeric(df["anterior"], downcast="float")
        df["consumo"] = df["consumo"]-df["anterior"]
        df['data'] = pd.to_datetime(df.data, format='%Y-%m-%d')

        days = df.groupby([df['data'].dt.date])['consumo'].sum()

        if len(days.index) > 3: 
            final = df.groupby(['cpf', df['data'].dt.date])['consumo'].sum().to_frame()
            final = final.reset_index()
            final['data'] = pd.to_datetime(final['data'], errors = 'coerce',format = '%Y-%m-%d').dt.strftime("%d-%b")
        else:
            final = df.groupby(['cpf', pd.Grouper(key='data',freq='H')])['consumo'].sum().to_frame()
            final = final.reset_index()
            final['data'] = pd.to_datetime(final['data'], errors = 'coerce',format = '%Y-%m-%d').dt.strftime("%a/%Hh")

        return final
    
    elif tipo == "estado":
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/details/query/estado"
        
        if estado == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}"}  
        else: param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "estado": f"{estado}"}  
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo"] = pd.to_numeric(df["consumo"], downcast="float")
        df["anterior"] = pd.to_numeric(df["anterior"], downcast="float")
        df["consumo"] = df["consumo"]-df["anterior"]
        df['data'] = pd.to_datetime(df.data, format='%Y-%m-%d')

        final = df.groupby(['estado', df['data'].dt.date])['consumo'].sum().to_frame()
        final = final.reset_index()
        final['data'] = pd.to_datetime(final['data'], errors = 'coerce',format = '%Y-%m-%d').dt.strftime("%d-%b")

        return final

    elif tipo == "cidade":
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/details/query/cidade"
        
        if cidade == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "estado": f"{estado}"}  
        else: param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "estado": f"{estado}", "cidade": f"{cidade}"}  
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo"] = pd.to_numeric(df["consumo"], downcast="float")
        df["anterior"] = pd.to_numeric(df["anterior"], downcast="float")
        df["consumo"] = df["consumo"]-df["anterior"]
        df['data'] = pd.to_datetime(df.data, format='%Y-%m-%d')

        final = df.groupby(['cidade', df['data'].dt.date])['consumo'].sum().to_frame()
        final = final.reset_index()
        final['data'] = pd.to_datetime(final['data'], errors = 'coerce',format = '%Y-%m-%d').dt.strftime("%d-%b")

        return final

    elif tipo == "bairro":
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/details/query/bairro"

        if bairro == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "estado": f"{estado}", "cidade": f"{cidade}"}  
        else: param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "estado": f"{estado}", "cidade": f"{cidade}", "bairro": f"{bairro}"}  
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo"] = pd.to_numeric(df["consumo"], downcast="float")
        df["anterior"] = pd.to_numeric(df["anterior"], downcast="float")
        df["consumo"] = df["consumo"]-df["anterior"]
        df['data'] = pd.to_datetime(df.data, format='%Y-%m-%d')

        final = df.groupby(['bairro', df['data'].dt.date])['consumo'].sum().to_frame()
        final = final.reset_index()
        final['data'] = pd.to_datetime(final['data'], errors = 'coerce',format = '%Y-%m-%d').dt.strftime("%d-%b")

        return final

def aggregates(startdate, enddate, tipo, cpf="", estado="", cidade="", bairro="",  granularity=""):
    method = "POST"    

    if tipo == "customer":   
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/aggregates/query/customer"

        if cpf == "1234": 
            if granularity == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}"}
            else: param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}"}
        else: param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}", "cpf": f"{cpf}"}
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo real"] = pd.to_numeric(df["consumo real"], downcast="float")
        df['data'] = pd.to_datetime(df.data, format='%Y-%m-%d')
        df['data'] = df['data'].dt.strftime('%m-%b')

        return df
    
    elif tipo == "estado":
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/aggregates/query/estado"
        
        if estado == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}"}
        if estado != "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}", "estado": f"{estado}"}   
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo real"] = pd.to_numeric(df["consumo real"], downcast="float")
        df['data'] = pd.to_datetime(df['data minimo'], format='%Y-%m-%d')
        df['data'] = df['data'].dt.strftime('%m-%b')

        return df

    elif tipo == "cidade":
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/aggregates/query/cidade"
        
        if cidade == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}", "estado": f"{estado}"}
        if cidade != "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}", "estado": f"{estado}", "cidade": f"{cidade}"}   
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo real"] = pd.to_numeric(df["consumo real"], downcast="float")
        df['data'] = pd.to_datetime(df['data minimo'], format='%Y-%m-%d')
        df['data'] = df['data'].dt.strftime('%m-%b')

        return df

    elif tipo == "bairro":
        url = "http://terguinator.pythonanywhere.com/api/v1/analytics/aggregates/query/bairro"
        
        if bairro == "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}", "estado": f"{estado}", "cidade": f"{cidade}"}
        if bairro != "": param = {"startdate": f"{startdate}", "enddate": f"{enddate}", "granularity": f"{granularity}", "estado": f"{estado}", "cidade": f"{cidade}", "bairro": f"{bairro}"} 
        pede_valores = run_request(method, url, param)

        df = pd.DataFrame(pede_valores['consumo'])
        df["consumo real"] = pd.to_numeric(df["consumo real"], downcast="float")
        df['data'] = pd.to_datetime(df['data minimo'], format='%Y-%m-%d')
        df['data'] = df['data'].dt.strftime('%m-%b')

        return df