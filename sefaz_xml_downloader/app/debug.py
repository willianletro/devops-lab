import xml.etree.ElementTree as ET
from logger import log_sefaz

def debug_resposta(xml):
    try:
        root = ET.fromstring(xml)
        ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

        cStat = root.find('.//ns:cStat', ns)
        xMotivo = root.find('.//ns:xMotivo', ns)
        ultNSU = root.find('.//ns:ultNSU', ns)
        maxNSU = root.find('.//ns:maxNSU', ns)
        docZip = root.findall('.//ns:docZip', ns)

        print("\n===== DEBUG SEFAZ =====")
        print("cStat:", cStat.text if cStat is not None else "N/A")
        print("Motivo:", xMotivo.text if xMotivo is not None else "N/A")
        print("ultNSU:", ultNSU.text if ultNSU is not None else "N/A")
        print("maxNSU:", maxNSU.text if maxNSU is not None else "N/A")
        print("Quantidade de docZip:", len(docZip))
        print("======================\n")
        
        inf_log_sefaz = {
            "cStat": cStat.text if cStat is not None else "N/A",
            "Motivo": xMotivo.text if xMotivo is not None else "N/A",
            "ultNSU": ultNSU.text if ultNSU is not None else "N/A",
            "maxNSU": maxNSU.text if maxNSU is not None else "N/A",
            "Quantidade de docZip": len(docZip)
        }
        
        log_sefaz(inf_log_sefaz)
        return cStat.text
    
    except Exception as e:
        print("Erro no debug:", e)