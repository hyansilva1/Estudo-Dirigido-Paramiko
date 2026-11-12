import conexao
import json
  


with open('inventario.json', 'r', encoding='utf-8') as arquivos:
    dados = json.load(arquivos)



cliente=conexao.conectar(dados[0])


codigo,saida,erro=conexao.executar(cliente,"whoami")


print(f"Código: {codigo}")
print(f"Saída: {saida}")
print(f"Error: {error}")