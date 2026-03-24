import logging
import os
from datetime import datetime

os.makedirs("/app/data/logs", exist_ok=True)

logging.basicConfig(
    filename="/app/data/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
    
    
def log_erro(chave, erro):
    os.makedirs("/app/logs", exist_ok=True)

    with open("/app/logs/erros_xml.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {chave} | {str(erro)}\n")