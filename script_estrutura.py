# script_estrutura_conteudo.py
import os
from datetime import datetime

try:
    import docx
except ImportError:
    docx = None

try:
    import odf.opendocument
    import odf.text
except ImportError:
    odf = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size/1024:.1f} KB"
    else:
        return f"{size/(1024**2):.1f} MB"

def read_file_preview(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in [".txt", ".py", ".md", ".csv", ".json"]:
            with open(file_path, "r", encoding="utf-8") as f:
                return "".join(f.readlines()[:10])  # primeiras 10 linhas
        elif ext == ".docx" and docx:
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs[:10]])
        elif ext == ".odt" and odf:
            doc = odf.opendocument.load(file_path)
            paras = doc.getElementsByType(odf.text.P)
            return "\n".join([p.firstChild.data for p in paras[:10] if p.firstChild])
        elif ext == ".pdf" and PyPDF2:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                pages = min(len(reader.pages), 3)
                return "\n".join([reader.pages[i].extract_text() for i in range(pages) if reader.pages[i].extract_text()])
        else:
            return "(conteúdo não legível ou binário)"
    except Exception as e:
        return f"(erro ao ler: {e})"

def walk_dir(path, prefix=""):
    entries = os.listdir(path)
    entries.sort()
    tree_lines = []
    for idx, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = "├─ " if idx < len(entries) - 1 else "└─ "
        if os.path.isdir(full_path):
            tree_lines.append(f"{prefix}{connector}{entry}/")
            tree_lines += walk_dir(full_path, prefix + ("│  " if idx < len(entries) - 1 else "   "))
        else:
            size = format_size(os.path.getsize(full_path))
            mtime = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M")
            tree_lines.append(f"{prefix}{connector}{entry} ({size}, modificado: {mtime})")
            # adiciona preview do conteúdo
            preview = read_file_preview(full_path)
            preview_lines = [f"{prefix}    {line}" for line in preview.splitlines()]
            tree_lines += preview_lines
    return tree_lines

if __name__ == "__main__":
    root_path = os.getcwd()
    print(f"Gerando estrutura detalhada com conteúdo do projeto em: {root_path}\n")
    tree = walk_dir(root_path)
    for line in tree:
        print(line)
    
    with open("project_structure_with_content.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(tree))
    
    print("\nÁrvore com conteúdo salva em project_structure_with_content.txt")
