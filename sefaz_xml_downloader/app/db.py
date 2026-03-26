import psycopg2
from config import POSTGRES_DB, POSTGRES_HOST,POSTGRES_USER,POSTGRES_PASSWORD

def conectar():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def xml_existe(chave):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM xmls WHERE chave = %s", (chave))
    existe = cur.fetchone()

    conn.close()
    return existe is not None


def salvar_xml_db(chave, cnpj, tipo, emissao, xml):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO xmls (chave, cnpj, tipo, emissao, xml, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (chave) DO NOTHING
    """, (chave, cnpj, tipo, emissao, xml, "BAIXADO"))

    conn.commit()
    conn.close()