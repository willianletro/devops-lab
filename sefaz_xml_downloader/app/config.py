import os
from dotenv import load_dotenv

load_dotenv()

CNPJS = os.getenv("CNPJS").split(",")
CERT_PATH = os.getenv("CERT_PATH")
CERT_PASSWORD = os.getenv("CERT_PASSWORD")
SEFAZ_URL = os.getenv("SEFAZ_URL")
SEFAZ_EVENTO_URL = os.getenv("SEFAZ_EVENTO_URL")

PASTA_XML = "data/xmls"