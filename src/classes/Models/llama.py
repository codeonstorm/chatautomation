from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3.2")





# set the LANGSMITH_API_KEY environment variable (create key in settings)
# from langchain import hub
# prompt = hub.pull("rlm/rag-prompt")