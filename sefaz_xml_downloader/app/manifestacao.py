import requests
import datetime
from requests_pkcs12 import post
from config import CERT_PATH, CERT_PASSWORD


def manifestar_nfe(cnpj, chave, cert, url):
    data_evento = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")

    xml = f"""
    <envEvento xmlns="http://www.portalfiscal.inf.br/nfe" versao="1.00">
        <idLote>1</idLote>
        <evento versao="1.00">
            <infEvento Id="ID210200{chave}01">
                <cOrgao>91</cOrgao>
                <tpAmb>1</tpAmb>
                <CNPJ>{cnpj}</CNPJ>
                <chNFe>{chave}</chNFe>
                <dhEvento>{data_evento}</dhEvento>
                <tpEvento>210210</tpEvento>
                <nSeqEvento>1</nSeqEvento>
                <verEvento>1.00</verEvento>
                <detEvento versao="1.00">
                    <descEvento>Confirmacao da Operacao</descEvento>
                </detEvento>
            </infEvento>
        </evento>
    </envEvento>
    """

    headers = {
        "Content-Type": "application/xml"
    }

    response = post(
        url,
        data=xml,
        pkcs12_filename=CERT_PATH,
        pkcs12_password=CERT_PASSWORD,
        headers=headers,
        verify=True
    )

    return response.text