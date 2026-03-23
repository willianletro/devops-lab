import xml.etree.ElementTree as ET

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

    except Exception as e:
        print("Erro no debug:", e)