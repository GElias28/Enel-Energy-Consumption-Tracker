import json, requests
import datetime

param = {}
def run_request(url, method, param=""):
    if method.upper() == "PUT": request = requests.put(url, json=param)  
    if request.text: response = json.loads(request.text)
    else: response = " "  
    print(f"{method.upper()}: {url}")
    print(param)
    print(f"Result: {request.status_code}")
    return {"response": response, "status_code": request.status_code}

def roundTime(dt=None, date_delta=datetime.timedelta(minutes=1), to='average'):
    round_to = date_delta.total_seconds()
    if dt is None: dt = datetime.now()
    seconds = (dt - dt.min).seconds
    if seconds % round_to == 0 and dt.microsecond == 0: rounding = (seconds + round_to / 2) // round_to * round_to
    else:
        if to == 'up': rounding = (seconds + dt.microsecond/1000000 + round_to) // round_to * round_to
        elif to == 'down': rounding = seconds // round_to * round_to
        else: rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, - dt.microsecond)


with open('input.txt', 'r') as input:
    for line in input:
        package = json.loads(line.rstrip())
        for idx, item in enumerate(package['consumo']):
            param.clear()            
            dt = datetime.datetime.strptime(package['consumo'][idx]['data'], '%Y-%m-%d %H:%M:%S')
            data = roundTime(dt=dt, date_delta=datetime.timedelta(minutes=15), to='average')
            consumo = package['consumo'][idx]['consumo']
            cpf = package['consumo'][idx]['cpf']            
            param = {"cpf": f"{cpf}", "data": f"{data}", "consumo": f"{consumo}"}           
            print("Registrando consumo...")
            url="http://terguinator.pythonanywhere.com/api/v1/consumo"
            method='PUT'
            request = run_request(url, method, param)
            status = request["status_code"]
            if status == 201 or status == 200:
                print("Consumo registrado com sucesso!")
                day = datetime.datetime.now().strftime("%x").replace("/", "-")
                file = open(f"{day}-requestlog.txt", 'a', encoding='utf-8')
                file.write(f"\nRequest: {method} {url}\nStatus Code: {status}\nParametros: {param}\n")
                file.close()
            else: print("ERRO! Consumo não foi registrado")