from requests_pkcs12 import post
from config import CERT_PATH, CERT_PASSWORD, SEFAZ_URL
from logger import log_info, log_error

def consultar_sefaz(cnpj, ult_nsu="000000000000000"):
    xml_envio = f"""
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <nfeDistDFeInteresse xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeDistribuicaoDFe">
        <nfeDadosMsg>
            <distDFeInt xmlns="http://www.portalfiscal.inf.br/nfe" versao="1.01">
            <tpAmb>1</tpAmb>
            <cUFAutor>31</cUFAutor>
            <CNPJ>{cnpj}</CNPJ>
            <distNSU>
                <ultNSU>{ult_nsu}</ultNSU>
            </distNSU>
            </distDFeInt>
        </nfeDadosMsg>
        </nfeDistDFeInteresse>
    </soap12:Body>
    </soap12:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8"
    }

    try:
        response = post(
            SEFAZ_URL,
            data=xml_envio,
            headers=headers,
            pkcs12_filename=CERT_PATH,
            pkcs12_password=CERT_PASSWORD
        )

        log_info("Consulta realizada com sucesso")
        return response.text

    except Exception as e:
        log_error(f"Erro na consulta: {e}")
        return None