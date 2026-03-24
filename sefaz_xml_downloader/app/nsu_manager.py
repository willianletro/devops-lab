import json
import os
from config import NSU_CONTROL


def carregar_nsu():
    if not os.path.exists(NSU_CONTROL):
        return {}
    
    with open(NSU_CONTROL, "r") as f:
        return json.load(f)


def salvar_nsu(cnpj, ult_nsu):
    data = carregar_nsu()
    data[cnpj] = ult_nsu

    with open(NSU_CONTROL, "w") as f:
        json.dump(data, f, indent=4)


def obter_nsu(cnpj):
    data = carregar_nsu()
    return data.get(cnpj, "000000000000000")