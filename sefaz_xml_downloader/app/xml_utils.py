import os
import base64
import gzip
import xml.etree.ElementTree as ET
from manifestacao import manifestar_nfe
from config import CERT_PATH, CERT_PASSWORD, SEFAZ_EVENTO_URL, PASTA_XML
from logger import log_erro
from db import xml_existe ,salvar_xml_db
from move_xml import processar


# 📁 cria estrutura de pastas
def criar_pastas(cnpj_base):
    base_path = os.path.join(PASTA_XML, cnpj_base)

    entrada = os.path.join(base_path, "entrada")
    saida = os.path.join(base_path, "saida")

    os.makedirs(entrada, exist_ok=True)
    os.makedirs(saida, exist_ok=True)

    return entrada, saida


# 🔑 extrai chave de acesso
def extrair_chave(xml_root):
    # tenta pegar do XML completo
    infNFe = xml_root.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe")
    if infNFe is not None:
        return infNFe.attrib.get("Id", "").replace("NFe", "")

    # tenta pegar do resumo
    chNFe = xml_root.find(".//{http://www.portalfiscal.inf.br/nfe}chNFe")
    if chNFe is not None:
        return chNFe.text

    return None


# 🧾 extrai CNPJ emitente
def extrair_emitente(xml_root):
    emit = xml_root.find(".//{http://www.portalfiscal.inf.br/nfe}emit")
    if emit is not None:
        cnpj = emit.find("{http://www.portalfiscal.inf.br/nfe}CNPJ")
        if cnpj is not None:
            return cnpj.text
    return None

def extrair_data_emissao(root):
    """
    Extrai a data de emissão do XML da NF-e
    """
    try:
        # namespace padrão da NF-e
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # tenta pegar dhEmi (mais completo)
        dhEmi = root.find('.//nfe:dhEmi', ns)

        if dhEmi is not None and dhEmi.text:
            return dhEmi.text

        # fallback para dEmi (modelo antigo)
        dEmi = root.find('.//nfe:dEmi', ns)

        if dEmi is not None and dEmi.text:
            return dEmi.text

        return None

    except Exception as e:
        print(f"Erro ao extrair data de emissão: {e}")
        return None




# 📥 extrai CNPJ destinatário
def extrair_destinatario(xml_root):
    dest = xml_root.find(".//{http://www.portalfiscal.inf.br/nfe}dest")
    if dest is not None:
        cnpj = dest.find("{http://www.portalfiscal.inf.br/nfe}CNPJ")
        if cnpj is not None:
            return cnpj.text
    return None


# 🔍 decide se é entrada ou saída
def identificar_tipo(xml_root, cnpj_consulta):
    emit = extrair_emitente(xml_root)
    dest = extrair_destinatario(xml_root)

    # se não achou (caso resNFe), tenta outro caminho
    if not emit or not dest:
        emit = xml_root.find(".//{http://www.portalfiscal.inf.br/nfe}CNPJ")
        if emit is not None:
            emit = emit.text

    if emit == cnpj_consulta:
        return "saida"
    elif dest == cnpj_consulta:
        return "entrada"
    else:
        return "entrada"  # fallback seguro


# 📦 extrai docZip
def extrair_doczips(xml):
    root = ET.fromstring(xml)
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    return root.findall(".//ns:docZip", ns)


# 💾 salva XML organizado
def salvar_xmls(doczips, cnpj):
    entrada_path, saida_path = criar_pastas(cnpj)
    
    sucesso_total = True  # 👈 controla o lote

    for doc in doczips:
        try:
            conteudo_zip = base64.b64decode(doc.text)
            xml_descompactado = gzip.decompress(conteudo_zip)

            root = ET.fromstring(xml_descompactado)

            chave = extrair_chave(root)
            data_emissao = extrair_data_emissao(root)
            
            if not chave:
                print("⚠️ Pulando XML sem chave")
                continue
            
            if xml_existe(chave):
                print(f"⚠️ Já processado: {chave}")
                continue
            
            tipo = identificar_tipo(root, cnpj)

            if not chave:
                print("⚠️ Não foi possível obter chave")
                continue

            if tipo == "entrada":
                caminho = entrada_path
            elif tipo == "saida":
                caminho = saida_path
            else:
                print("⚠️ Tipo desconhecido")
                continue

            arquivo = os.path.join(caminho, f"{chave}.xml")

            # 🔔 manifestação segura
            if tipo == "entrada" and not os.path.exists(arquivo):
                try:
                    print(f"🔔 Manifestando nota: {chave}")
                    manifestar_nfe(
                        cnpj,
                        chave,
                        cert=CERT_PATH,
                        url=SEFAZ_EVENTO_URL
                    )
                except Exception as e:
                    sucesso_total = False
                    log_erro(chave, e)
                    continue
                        
            
            if not os.path.exists(arquivo):
                with open(arquivo, "wb") as f:
                    f.write(xml_descompactado)

                print(f"✅ XML salvo: {arquivo}")
            else:
                print(f"⚠️ XML já existe: {arquivo}")
            
            # 🔥 Converter antes de salvar no banco
            xml_texto = xml_descompactado.decode("utf-8", errors="replace")
            
            # 💾 SALVAR NO BANCO (ESSENCIAL)
            salvar_xml_db(
                chave,
                cnpj,
                tipo,
                data_emissao,
                xml_texto
                
            )
            processar()    
                

        except Exception as e:
            sucesso_total = False
            log_erro("XML_DESCONHECIDO", e)
            
    return sucesso_total
            
def extrair_ult_nsu(xml):
    import xml.etree.ElementTree as ET

    try:
        root = ET.fromstring(xml)
        ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

        ult_nsu = root.find('.//ns:ultNSU', ns)

        if ult_nsu is not None:
            return ult_nsu.text

    except Exception as e:
        print("Erro ao extrair ultNSU:", e)

    return None