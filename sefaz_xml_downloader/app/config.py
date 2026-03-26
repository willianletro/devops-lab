import os
from dotenv import load_dotenv

load_dotenv()

CNPJS = os.getenv("CNPJS").split(",")
CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")
SEFAZ_URL = os.getenv("SEFAZ_URL")
SEFAZ_EVENTO_URL = os.getenv("SEFAZ_EVENTO_URL")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB= os.getenv("POSTGRES_DB")
POSTGRES_HOST= os.getenv("POSTGRES_HOST")
POSTGRES_PORT= os.getenv("POSTGRES_PORT")

PASTA_XML = os.getenv("PASTA_XML")
NSU_CONTROL = os.getenv("NSU_CONTROL")
LOGS = os.getenv("LOGS")
#testepipelines