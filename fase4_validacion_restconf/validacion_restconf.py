import requests
import json
import yaml
import urllib3

# Desactivar advertencias de certificados autofirmados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Cargar las variables corporativas
with open("../vars/vars_001V-14.yaml", "r") as f:
    vars_data = yaml.safe_load(f)

print("Iniciando auditoria RESTCONF...")

router_ip = vars_data['router']['ip']
auth = (vars_data['router']['usuario'], vars_data['router']['password'])
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Definir las 4 URLs (Endpoints) de consulta
urls = {
    "hostname": f"https://{router_ip}/restconf/data/Cisco-IOS-XE-native:native/hostname",
    "loopback": f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback14",
    "interfaces": f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1",
    "ntp": f"https://{router_ip}/restconf/data/Cisco-IOS-XE-native:native/ntp"
}

resultados = {}

# 2. Hacer las 4 consultas y guardar los JSON (Evidencias E17, E18, E19, E20)
for clave, url in urls.items():
    try:
        response = requests.get(url, auth=auth, headers=headers, verify=False)
        data = response.json()
        resultados[clave] = json.dumps(data)
        
        # Guardar en archivo
        filename = f"responses/get_{clave}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        resultados[clave] = ""
        print(f"Error consultando {clave}: {e}")

# 3. Validacion de Parametros
print("\n=== RESULTADOS DE VALIDACION RESTCONF ===")
checks = 0

if vars_data['cliente']['hostname'] in resultados['hostname']:
    print(f"[OK] Hostname verificado via API: {vars_data['cliente']['hostname']}")
    checks += 1
else:
    print("[FAIL] Hostname incorrecto")

if vars_data['loopback_ip'] in resultados['loopback']:
    print(f"[OK] IP Loopback verificada via API: {vars_data['loopback_ip']}")
    checks += 1
else:
    print("[FAIL] IP Loopback incorrecta")

if vars_data['descripcion_wan'] in resultados['interfaces']:
    print(f"[OK] Descripcion WAN verificada via API: {vars_data['descripcion_wan']}")
    checks += 1
else:
    print("[FAIL] Descripcion WAN incorrecta")

if vars_data['ntp_server'] in resultados['ntp']:
    print(f"[OK] Servidor NTP verificado via API: {vars_data['ntp_server']}")
    checks += 1
else:
    print("[FAIL] Servidor NTP incorrecto")

print("\n-----------------------------------------")
print(f"Total Criterios Cumplidos: {checks}/4")
if checks == 4:
    print("Estado Final: CONFORME")
else:
    print("Estado Final: NO CONFORME")
print("-----------------------------------------")
