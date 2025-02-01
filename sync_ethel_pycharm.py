import requests
import os
import time

# URL do repositório ou local onde as atualizações do Ethel são armazenadas
URL_CODIGO = "https://seu_servidor_ou_api/aqui"
CAMINHO_ARQUIVO = "C:/Users/FSA-SILVA/PycharmProjects/PythonProject4/robo_treino_mestrado.py"

def baixar_codigo():
    try:
        response = requests.get(URL_CODIGO)
        if response.status_code == 200:
            with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
                arquivo.write(response.text)
            print("✅ Código atualizado com sucesso!")
            return True
        else:
            print(f"⚠ Erro ao baixar código: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠ Erro na sincronização: {str(e)}")
        return False

def executar_codigo():
    print("▶ Executando o código atualizado...")
    os.system(f"python {CAMINHO_ARQUIVO}")

while True:
    print("🔄 Verificando por atualizações...")
    if baixar_codigo():
        executar_codigo()
    time.sleep(60)  # Aguarda 60 segundos antes de buscar nova atualização
