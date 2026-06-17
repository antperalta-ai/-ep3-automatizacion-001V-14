import yaml
import xml.dom.minidom
from ncclient import manager

# 1. Cargar las variables corporativas
with open("../vars/vars_001V-14.yaml", "r") as f:
    vars_data = yaml.safe_load(f)

print("Iniciando auditoria NETCONF...")

# 2. Conectar al router via NETCONF (Puerto 830)
with manager.connect(
    host=vars_data['router']['ip'],
    port=830,
    username=vars_data['router']['usuario'],
    password=vars_data['router']['password'],
    hostkey_verify=False,
    device_params={'name': 'iosxe'}
) as m:
    
    # 3. Obtener la configuracion en ejecucion (running-config)
    print("Descargando configuracion en formato XML...")
    netconf_reply = m.get_config(source='running')
    xml_data = netconf_reply.xml

    # 4. Guardar el XML puro (Evidencia E13)
    with open("evidencias/rpc_reply_raw.xml", "w") as f:
        f.write(xml.dom.minidom.parseString(xml_data).toprettyxml())

# 5. Validacion de Parametros
print("\n=== RESULTADOS DE VALIDACION NETCONF ===")
checks = 0

if vars_data['cliente']['hostname'] in xml_data:
    print(f"[OK] Hostname verificado: {vars_data['cliente']['hostname']}")
    checks += 1
else:
    print("[FAIL] Hostname incorrecto")

if vars_data['ntp_server'] in xml_data:
    print(f"[OK] Servidor NTP verificado: {vars_data['ntp_server']}")
    checks += 1
else:
    print("[FAIL] Servidor NTP incorrecto")

if "ACCESO RESTRINGIDO" in xml_data:
    print("[OK] Banner corporativo verificado")
    checks += 1
else:
    print("[FAIL] Banner incorrecto")

if vars_data['descripcion_wan'] in xml_data:
    print(f"[OK] Descripcion WAN verificada: {vars_data['descripcion_wan']}")
    checks += 1
else:
    print("[FAIL] Descripcion WAN incorrecta")

if vars_data['loopback_ip'] in xml_data:
    print(f"[OK] IP de Loopback verificada: {vars_data['loopback_ip']}")
    checks += 1
else:
    print("[FAIL] IP de Loopback incorrecta")

print("\n-----------------------------------------")
print(f"Total Criterios Cumplidos: {checks}/5")
if checks == 5:
    print("Estado Final: CONFORME")
else:
    print("Estado Final: NO CONFORME")
print("-----------------------------------------")
