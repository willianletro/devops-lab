from sefaz_client import consultar_sefaz
from config import CNPJS
from logger import log_info
from xml_utils import extrair_doczips, salvar_xmls, extrair_ult_nsu
from nsu_manager import obter_nsu, salvar_nsu
from debug import debug_resposta
from move_xml import processar


def main():
    log_info("Iniciando processo...")

    for cnpj in CNPJS:
        print(f"\nConsultando CNPJ: {cnpj}")

        # 🔑 pega último NSU salvo
        ult_nsu = obter_nsu(cnpj)

        print(f"Usando ultNSU: {ult_nsu}")

        # 🔄 consulta SEFAZ
        resposta = consultar_sefaz(cnpj, ult_nsu)


        if resposta:
            # 🔍 DEBUG
            debug_resposta(resposta)

            # 💾 SALVAR NOVO NSU (AQUI 👇)
            novo_nsu = extrair_ult_nsu(resposta)

            if novo_nsu:
                print(f"Novo NSU encontrado: {novo_nsu}")
                salvar_nsu(cnpj, novo_nsu)

            # 📦 extrair XMLs
            doczips = extrair_doczips(resposta)

            if doczips:
                sucesso = salvar_xmls(doczips, cnpj)

                if sucesso:
                    novo_nsu = extrair_ult_nsu(resposta)
                    salvar_nsu(cnpj, novo_nsu)
                    print(f"✅ NSU atualizado: {novo_nsu}")
                else:
                    print("❌ Erro no lote, NSU NÃO atualizado")
            else:
                print("Nenhum XML encontrado")

    log_info("Processo finalizado")


if __name__ == "__main__":
    main()