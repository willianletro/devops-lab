import os
import shutil
import time
from config import PASTA_XML

MAPEAMENTO = {
    "02912729000160/entrada": "/mnt/consinco/01_MATRIZ",
    "02912729000321/entrada": "/mnt/consinco/03_BROMELIAS",
    "02912729000240/entrada": "/mnt/consinco/06_DISTRITO",
    "02912729000755/entrada": "/mnt/consinco/09_MVIANA"
}

def processar():
    
    for cnpj, destino in MAPEAMENTO.items():
        origem = os.path.join(PASTA_XML, cnpj)

        if not os.path.exists(origem):
            continue

        for arquivo in os.listdir(origem):
            if not arquivo.endswith(".xml"):
                continue

            origem_arquivo = os.path.join(origem, arquivo)
            destino_arquivo = os.path.join(destino, arquivo)
            
            try:
                # evita duplicado
                if os.path.exists(destino_arquivo):
                    continue

                # copia
                shutil.copy(origem_arquivo, destino_arquivo)

                print(f"✔ Enviado: {arquivo}")

                # remove origem
                os.remove(origem_arquivo)

            except Exception as e:
                print(f"❌ Erro: {arquivo} -> {e}")
    #time.sleep()
#if __name__ == "__main__":
    #print(r"\\192.168.0.211\degrau xml\01_MATRIZ")
    #processar()
        