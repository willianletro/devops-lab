import json
import os

ARQUIVO_NSU = "/app/nsu_control.json"


def carregar_nsu():
    if not os.path.exists(ARQUIVO_NSU):
        return {}
    
    with open(ARQUIVO_NSU, "r") as f:
        return json.load(f)


def salvar_nsu(cnpj, ult_nsu):
    data = carregar_nsu()
    data[cnpj] = ult_nsu

    with open(ARQUIVO_NSU, "w") as f:
        json.dump(data, f, indent=4)


def obter_nsu(cnpj):
    data = carregar_nsu()
    return data.get(cnpj, "000000000000000")