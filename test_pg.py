import os
from dotenv import load_dotenv
import psycopg2

# 1️⃣ Carregar variáveis do .env
load_dotenv()

# 2️⃣ Pegar a URL
DATABASE_URL = os.getenv("DATABASE_URL")
print("Usando DATABASE_URL:", DATABASE_URL)

# 3️⃣ Conectar
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("Conexão bem-sucedida:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("Erro na conexão:", e)
