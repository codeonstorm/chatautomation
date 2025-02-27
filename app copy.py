from dotenv import load_dotenv
import os
os.environ["USER_AGENT"] = "MyCustomUserAgent"
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_ollama import ChatOllama
from src.classes.QdrantManager import QdrantManager

from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState, StateGraph


from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.tools import tool

from src.classes.QdrantManager import QdrantManager
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
load_dotenv()

llm = ChatOllama(model="llama3.2", temperature=1)

# Load and chunk contents of the blog
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
all_splits = text_splitter.split_documents(docs)


# embeddings = OllamaEmbeddings(model="llama3.2")

client = QdrantClient(url=os.getenv("QDRANT_CLIENT_URL"), api_key=os.getenv("QDRANT_CLIENT_API_KEY"))
client.create_collection(
    collection_name="ertrt",
    vectors_config=VectorParams(size=128, distance=Distance.COSINE)  # Adjust size & distance as needed
)
# _ = vector_store.add_documents(documents=all_splits)


# Define state for application
# class State(TypedDict):
#     question: str
#     context: List[Document]
#     answer: str


# # Define application steps
# def retrieve(state: State):
#     retrieved_docs = vector_store.similarity_search(state["question"])
#     return {"context": retrieved_docs}


# def generate(state: State):
#     docs_content = "\n\n".join(doc.page_content for doc in state["context"])
#     messages = prompt.invoke({"question": state["question"], "context": docs_content})
#     response = llm.invoke(messages)
#     return {"answer": response.content}


# # Compile application and test
# graph_builder = StateGraph(State).add_sequence([retrieve, generate])
# graph_builder.add_edge(START, "retrieve")
# graph = graph_builder.compile()


# # Define prompt for question-answering
# prompt = hub.pull("rlm/rag-prompt")
# print("prompt", prompt)

# response = graph.invoke({"question": "What is Task Decomposition?"})
# print(response["answer"])




# #  new
# @tool(response_format="content_and_artifact")
# def retrieve(query: str):
#     """Retrieve information related to a query."""
#     # print("query===", query)
#     # Index chunks
#     qdrantManager = QdrantManager()
#     vector_store = qdrantManager.get_vector_store("chatbot")
#     # print(vector_store)
#     # _ = vector_store.add_documents(documents=all_splits)
#     retrieved_docs = vector_store.similarity_search(query, k=2)
#     serialized = "\n\n".join(
#         (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
#         for doc in retrieved_docs
#     )
#     return serialized, retrieved_docs
    
# graph_builder = StateGraph(MessagesState)


# # Step 1: Generate an AIMessage that may include a tool-call to be sent.
# def query_or_respond(state: MessagesState):
#     """Generate tool call for retrieval or respond."""
#     llm_with_tools = llm.bind_tools([retrieve])
#     response = llm_with_tools.invoke(state["messages"])
#     # MessagesState appends messages to state instead of overwriting
#     return {"messages": [response]}

 
# # Step 2: Execute the retrieval.
# tools = ToolNode([retrieve])

# def custom_tools_condition(state: MessagesState):
#     """Check if the AI response contains a tool call."""
#     last_message = state["messages"][-1]
    
#     print("Checking tools_condition... Last Message:", last_message)  # Debugging

#     # if last_message.type == "ai" and last_message.tool_calls:
#     print("Condition met: Redirecting to 'tools'")  # Debugging
#     return "tools"
    
#     # print("Condition NOT met: Ending")  # Debugging
#     # return END


# # Step 3: Generate a response using the retrieved content.
# def generate(state: MessagesState):
#     """Generate answer."""
#     print("genrate")
#     # Get generated ToolMessages
#     recent_tool_messages = []
#     for message in reversed(state["messages"]):
#         if message.type == "tool":
#             recent_tool_messages.append(message)
#         else:
#             break
#     tool_messages = recent_tool_messages[::-1]

#     # Format into prompt
#     docs_content = "\n\n".join(doc.content for doc in tool_messages)
#     system_message_content = (
#         "You are an assistant for question-answering tasks. "
#         "Use the following pieces of retrieved context to answer "
#         "the question. If you don't know the answer, say that you "
#         "don't know. Use three sentences maximum and keep the "
#         "answer concise."
#         "\n\n"
#         f"{docs_content}"
#     )
#     conversation_messages = [
#         message
#         for message in state["messages"]
#         if message.type in ("human", "system")
#         or (message.type == "ai" and not message.tool_calls)
#     ]
#     prompt = [SystemMessage(system_message_content)] + conversation_messages

#     # Run
#     response = llm.invoke(prompt)
#     return {"messages": [response]}

# # ///////
# from langgraph.graph import END
# from langgraph.prebuilt import ToolNode, tools_condition

# graph_builder.add_node(query_or_respond)
# graph_builder.add_node(tools)
# graph_builder.add_node(generate)

# graph_builder.set_entry_point("query_or_respond")
# graph_builder.add_conditional_edges(
#     "query_or_respond",
#     # tools_condition,
#     custom_tools_condition,
#     {"tools": "tools", END: END},
# )
# # graph_builder.add_edge("query_or_respond", "tools")
# graph_builder.add_edge("tools", "generate")
# graph_builder.add_edge("generate", END)

# graph = graph_builder.compile()

# from IPython.display import Image, display

# graph_image = graph.get_graph().draw_mermaid_png()
# with open("graph_image.png", "wb") as f:
#     f.write(graph_image)


# input_message = "Hello"

# for step in graph.stream(
#     {"messages": [{"role": "user", "content": input_message}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()



# input_message = "What is Task Decomposition?"

# for step in graph.stream(
#     {"messages": [{"role": "user", "content": input_message}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()