from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# LLM
llm = OllamaLLM(model="gemma3:latest")

# Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# Documentos para indexar
documentos = [
    "LangChain é uma biblioteca para construir sistemas LLMs encadeados.",
    "O RAG permite gerar respostas usando informações de documentos externos.",
    "Ollama é um modelo que pode ser usado localmente para LLMs e embeddings."
]

# Dividir textos em chunks
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
docs_chunks = text_splitter.split_text(" ".join(documentos))

# Criar índice FAISS
vectorstore = FAISS.from_texts(docs_chunks, embeddings)

# Função RAG
def consulta_rag(query: str):
    resultados = vectorstore.similarity_search(query, k=2)
    context = " ".join([r.page_content for r in resultados])
    resposta = llm.invoke(f"Use o contexto abaixo para responder a pergunta:\n{context}\nPergunta: {query}")
    return resposta

# Teste
pergunta = "O que é RAG?"
print(consulta_rag(pergunta))
