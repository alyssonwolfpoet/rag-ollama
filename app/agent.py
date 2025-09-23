# app/agent.py
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from app.vectorstore import get_vectorstore
from app.utils import processing

# Inicializa LLM multimodal e embeddings
llm = Ollama(model="gemma3")
embeddings = OllamaEmbeddings(model="gemma3")

# Inicializa PGVector
vectorstore = get_vectorstore(embeddings)
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# Ferramentas do agente
search = DuckDuckGoSearchRun()
tools = [
    Tool(name="RAG_Documentos", func=lambda q: qa_chain.run(q), description="Responde perguntas sobre documentos carregados"),
    Tool(name="BuscarWeb", func=search.run, description="Busca informações na web"),
    Tool(name="DataHora", func=processing.data_hora_atual, description="Retorna a data e hora atual"),
    Tool(name="Calculadora", func=processing.calcular_expressao, description="Resolve cálculos matemáticos simples"),
    Tool(name="GerarPDF", func=processing.gerar_pdf, description="Gera PDF a partir do texto"),
    Tool(name="GerarExcel", func=processing.gerar_excel, description="Gera Excel a partir do texto"),
]

# Inicializa agente zero-shot
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
