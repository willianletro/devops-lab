import logging
import os
from datetime import datetime
from config import LOGS

os.makedirs(LOGS, exist_ok=True)

logging.basicConfig(
    filename= os.path.join(LOGS, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
    
    
def log_erro(chave, erro):
    #os.makedirs(LOGS, exist_ok=True)
    
    logerr = os.path.join(LOGS, "erros_xml.log")

    with open(logerr, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {chave} | {str(erro)}\n")
        
        
def log_sefaz(inf):
    
    logerr = os.path.join(LOGS, "log_sefaz.log")
    
    texto = f"""
    ===== DEBUG SEFAZ =====
    Data: {datetime.now()}

    cStat: {inf.get("cstat")}
    Motivo: {inf.get("motivo")}
    ultNSU: {inf.get("ult_nsu")}
    maxNSU: {inf.get("max_nsu")}
    Quantidade de docZip: {inf.get("qtd_doczip")}

    ======================
    """

    with open(logerr, "a", encoding="utf-8") as f:
        f.write(texto)