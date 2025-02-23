from dotenv import load_dotenv
import os
os.environ["USER_AGENT"] = "MyCustomUserAgent"
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from typing_extensions import List, TypedDict
from src.classes.QdrantManager import QdrantManager
from langgraph.graph import MessagesState

# Load environment variables
load_dotenv()

class ChatbotPipeline:
    def __init__(self, model_name="llama3.2", temperature=1):
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        self.graph_builder = StateGraph(MessagesState)
        self._setup_graph()

    @tool(response_format="content_and_artifact")
    def retrieve(self, query: str):
        """Retrieve information related to a query."""
        try:
            qdrant_manager = QdrantManager()
            vector_store = qdrant_manager.get_vector_store("chatbot")
            retrieved_docs = vector_store.similarity_search(query, k=2)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized, retrieved_docs
        except Exception as e:
            return f"Error retrieving data: {str(e)}", []

    def query_or_respond(self, state: MessagesState):
        """Generate tool call for retrieval or respond."""
        llm_with_tools = self.llm.bind_tools([self.retrieve])
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def custom_tools_condition(self, state: MessagesState):
        """Check if the AI response contains a tool call."""
        last_message = state["messages"][-1]
        # if last_message.type == "ai" and last_message.tool_calls:
        return "tools"
        return END

    def generate_response(self, state: MessagesState):
        """Generate answer based on retrieved content."""
        try:
            recent_tool_messages = [msg for msg in reversed(state["messages"]) if msg.type == "tool"]
            docs_content = "\n\n".join(doc.content for doc in reversed(recent_tool_messages))
            system_message_content = (
                "You are an assistant for question-answering tasks. Use the following pieces "
                "of retrieved context to answer the question. If you don't know the answer, "
                "say that you don't know. Use three sentences maximum and keep the answer concise."
                f"\n\n{docs_content}"
            )
            prompt = [SystemMessage(system_message_content)] + [msg for msg in state["messages"] if msg.type in ("human", "system") or (msg.type == "ai" and not msg.tool_calls)]
            response = self.llm.invoke(prompt)
            return {"messages": [response]}
        except Exception as e:
            return {"messages": [SystemMessage(f"Error generating response: {str(e)}")]}

    def _setup_graph(self):
        """Setup the LangGraph workflow."""
        self.graph_builder.add_node(self.query_or_respond)
        self.graph_builder.add_node(ToolNode([self.retrieve]))
        self.graph_builder.add_node(self.generate_response)
        self.graph_builder.set_entry_point("query_or_respond")
        self.graph_builder.add_conditional_edges(
            "query_or_respond", self.custom_tools_condition, {"tools": "tools", END: END}
        )
        self.graph_builder.add_edge("tools", "generate_response")
        self.graph_builder.add_edge("generate_response", END)
        self.graph = self.graph_builder.compile()

    def run(self, input_message: str):
        """Execute the chatbot pipeline with a user message."""
        try:
            for step in self.graph.stream(
                {"messages": [{"role": "user", "content": input_message}]},
                stream_mode="values",
            ):
                step["messages"][-1].pretty_print()
        except Exception as e:
            print(f"Pipeline execution error: {str(e)}")

if __name__ == "__main__":
    chatbot = ChatbotPipeline()
    chatbot.run("What is Task Decomposition?")