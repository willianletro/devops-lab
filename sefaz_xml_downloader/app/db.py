import psycopg2

def conectar():
    return psycopg2.connect(
        host="db",
        database="devopsdb",
        user="devops",
        password="devops"
    )

def xml_existe(chave):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM xmls WHERE chave = %s", (chave,))
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
    """, (chave, cnpj, tipo, emissao, xml.decode("utf-8"), "BAIXADO"))

    conn.commit()
    conn.close()