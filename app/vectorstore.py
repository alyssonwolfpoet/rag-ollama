# app/vectorstore.py
from langchain_community.vectorstores import PGVector
from sqlalchemy import create_engine, text
import os

PG_CONN_INFO = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:ifce@localhost:5432/rag")

def get_vectorstore(embedding_function):
    """
    Inicializa PGVector e cria extensão 'vector' se não existir.
    """
    engine = create_engine(PG_CONN_INFO)
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()

    # Retorna o objeto PGVector pronto para uso
    return PGVector(
        collection_name="documentos",
        connection_string=PG_CONN_INFO,
        embedding_function=embedding_function.embed_query
    )
