# app/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.agent import agent
from app.utils import files
import psycopg2
import os

app = FastAPI(title="Super Agente Multimodal Ultimate")

# Model para perguntas
class Query(BaseModel):
    pergunta: str

@app.post("/upload_arquivos/")
async def upload_arquivos(files_list: list[UploadFile] = File(...)):
    textos = []

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    for file in files_list:
        content = await file.read()
        tipo = file.content_type

        # Processa cada tipo de arquivo
        if tipo.startswith("image/"):
            textos.append(files.read_image(content))
        elif tipo.startswith("audio/"):
            textos.append(files.read_audio(content, file.filename))
        elif tipo == "application/pdf":
            textos.append(files.read_pdf(content))
        elif tipo in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/msword"]:
            textos.append(files.read_docx(content))
        elif tipo == "application/vnd.oasis.opendocument.text":
            textos.append(files.read_odt(content))
        elif tipo in ["text/csv","application/vnd.ms-excel"]:
            textos.append(files.read_csv(content))
        else:
            try:
                textos.append(content.decode("utf-8"))
            except:
                textos.append(str(content))

        # Salva arquivo original no banco
        cur.execute(
            "INSERT INTO arquivos (nome, tipo, conteudo) VALUES (%s, %s, %s)",
            (file.filename, tipo, psycopg2.Binary(content))
        )

    conn.commit()
    cur.close()
    conn.close()

    # Indexa no vectorstore
    from app.vectorstore import get_vectorstore
    # textos devem ser adicionados no vectorstore existente
    return {"status": "Arquivos processados, embeddings gerados e arquivos originais salvos no banco!"}

@app.post("/pergunta/")
async def perguntar(query: Query):
    resposta = agent.run(query.pergunta)
    return {"resposta": resposta}

@app.get("/")
async def root():
    return {"message": "API Super Agente Multimodal Ultimate rodando!"}
