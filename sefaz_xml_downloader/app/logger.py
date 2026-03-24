import logging
import os
from datetime import datetime

os.makedirs("/data/logs", exist_ok=True)

logging.basicConfig(
    filename="/data/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
    
    
def log_erro(chave, erro):
    os.makedirs("logs", exist_ok=True)

    with open("/logs/erros_xml.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {chave} | {str(erro)}\n")