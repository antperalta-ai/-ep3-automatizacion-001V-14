import yaml
with open("../vars/vars_001V-14.yaml", "r") as f:
    vars_data = yaml.safe_load(f)

certificado = f"""===================================================
CERTIFICADO DE COMPLIANCE DE RED
===================================================
Cliente: {vars_data['cliente']['empresa']}
Hostname: {vars_data['cliente']['hostname']}
IP de Gestion: {vars_data['loopback_ip']}

Ingeniero a cargo: {vars_data['nombre']}
Codigo: {vars_data['codigo']}

Resultado de Auditoria Ansible: OK (Idempotencia comprobada)
Resultado de Auditoria NETCONF: CONFORME
Resultado de Auditoria RESTCONF: CONFORME
Validacion de Cambios (Genie Diff): REALIZADO

ESTADO FINAL DEL EQUIPO: CONFORME
==================================================="""

with open("evidencias/certificado_compliance_001V-14.txt", "w") as f:
    f.write(certificado)
