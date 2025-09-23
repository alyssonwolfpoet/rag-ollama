# app/utils/files.py
import io
import pdfplumber
import docx
from odf.opendocument import load
from odf import text, teletype
from PIL import Image
import whisper
import os

TEMP_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def read_pdf(file_content: bytes) -> str:
    texto = ""
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            texto += page.extract_text() + "\n"
    return texto.strip()

def read_docx(file_content: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_content))
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def read_odt(file_content: bytes) -> str:
    odt_doc = load(io.BytesIO(file_content))
    allparas = odt_doc.getElementsByType(text.P)
    return "\n".join([teletype.extractText(p) for p in allparas]).strip()

def read_csv(file_content: bytes) -> str:
    import pandas as pd
    df = pd.read_csv(io.BytesIO(file_content))
    return df.to_string(index=False)

def read_image(file_content: bytes) -> bytes:
    # Retorna bytes para embeddings multimodais do modelo Gemma3
    return file_content

def read_audio(file_content: bytes, filename: str) -> str:
    """
    Salva o áudio temporariamente em temp/ e transcreve usando Whisper.
    """
    path = os.path.join(TEMP_DIR, filename)
    with open(path, "wb") as f:
        f.write(file_content)
    model = whisper.load_model("base")
    result = model.transcribe(path)
    os.remove(path)
    return result["text"]
