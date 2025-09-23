# app/utils/processing.py
from fpdf import FPDF
import pandas as pd
from datetime import datetime

def gerar_pdf(texto: str, filename="saida.pdf") -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    pdf.output(filename)
    return filename

def gerar_excel(texto: str, filename="saida.xlsx") -> str:
    df = pd.DataFrame({"Conteúdo": texto.split("\n")})
    df.to_excel(filename, index=False)
    return filename

def data_hora_atual(_) -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def calcular_expressao(expr: str) -> str:
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Erro: {str(e)}"
