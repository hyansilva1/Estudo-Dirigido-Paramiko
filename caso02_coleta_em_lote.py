import csv
import json
from concurrent.futures import ThreadPoolExecutor
from conexao import conectar, executar

COLUNAS = ["nome", "usuario", "hostname", "kernel", "uptime", "status"]

def coletar(disp):
    registro = {c: "" for c in COLUNAS}
    registro["nome"] = disp["nome"]
    try:
        cliente = conectar(disp)
        try:
            registro["usuario"] = executar(cliente, "whoami")[1]
            registro["hostname"] = executar(cliente, "hostname")[1]
            registro["kernel"] = executar(cliente, "uname -r")[1]
            registro["uptime"] = executar(cliente, "uptime -p")[1]
            registro["status"] = "OK"
        finally:
            cliente.close()
    except Exception as e:
        registro["status"] = f"FALHA: {type(e).__name__}"
    return registro

with open("inventario.json", encoding="utf-8") as f:
    inventario = json.load(f)

with ThreadPoolExecutor(max_workers=10) as pool:
    resultados = list(pool.map(coletar, inventario))

with open("inventario_coletado.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=COLUNAS)
    escritor.writeheader()
    escritor.writerows(resultados)

for r in resultados:
    print(f"{r['nome']:<4} {r['status']:<12} {r['usuario']:<6} {r['uptime']}")