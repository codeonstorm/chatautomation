class Template:
  """Static class for managing prompt templates and instructions"""
  
  @staticmethod
  def get_system_prompt():
    """Returns the system prompt for the AI"""
    return """You are an AI programming assistant.
    When asked for your name, you must respond with "GitHub Copilot".
    Follow Microsoft content policies.
    Keep responses focused on software development."""

  # @staticmethod
  # def get_instruction_template():
  #   """Returns the base instruction template"""
  #   return """
  #   Instructions:
  #   {instruction}

  #   Context:
  #   {context}
  #   """

  # @staticmethod
  # def format_instruction(instruction: str, context: str = "") -> str:
  #   """Formats the instruction with given context"""
  #   template = Prompt.get_instruction_template()
  #   return template.format(instruction=instruction, context=context)

  # @staticmethod
  # def condense_question_system_template() -> dict:
  #   return {
  #       "role": "system",
  #       "content": (
  #           "Rewrite the user's latest question as a standalone question.\n"
  #           "Use previous conversation only if needed.\n"
  #           "Only return the standalone question. No explanation. No formatting. No extra words.\n"
  #           "If the user query is incomplete or unclear, return: 'Please clarify your question.'"
  #       )
  #   }
  @staticmethod
  def condense_question_system_template() -> dict:
    return {
        "role": "system",
        "content": (
              "You are a helpful assistant.\n"
              "When the user provides a message, your task is to rewrite it into a clear, concise standalone question.\n"
              "If you truly can't guess the question, ask for clarification.\n\n"
              # "End your question with a question mark (?).\n"
              "Respond with ONLY the rewritten question."
              "- Do NOT answer the question.\n"
              "- Do NOT explain anything.\n"
              "- Do NOT explain anything.\n"
              "- Do NOT add formatting, markdown, or symbols like *, ``, quotes, or emojis.\n"
          )
        # "content": (
        #     "##STRICT_MODE: Follow all instructions exactly and without deviation.\n\n"
        #     "Your ONLY task is to rewrite the user's latest message into a standalone question.\n"
        #     "Use previous user messages ONLY if absolutely necessary to understand context.\n\n"
        #     "##DO_NOT:\n"
        #     "- Do NOT answer the question.\n"
        #     "- Do NOT explain anything.\n"
        #     "- Do NOT repeat assistant messages.\n"
        #     "- Do NOT use formatting (no lists, no bold, no bullet points).\n"
        #     "- Do NOT add extra words.\n\n"
        #     "##ONLY_RETURN:\n"
        #     "- A single, clear, standalone question.\n"
        #     "- If the user input is incomplete or unclear, return EXACTLY: Please clarify your question.\n\n"
        #     "##IMPORTANT:\n"
        #     "- Respond with ONLY the final standalone question. Nothing else."
        # )
    }




    

  
  @staticmethod
  def system_prompt_for_tools_intro() -> str:
    return {
      "role": "system",
      "content": "\n".join([
          "You are a BuyBot AI chatbot. You must select only one most relevant tool from the **provided tools.",
          "Tools Information helps you in selection:",
          "- greeting: Use for replies like: Hi, Hello, Thanks, Bye!",
          "- retriever: Use for questions asking for facts, product info, knowledge, or data from a knowledge base or data store.",
          "",
          # "You must convert the user's latest message into a **standalone question** that can be passed to the tool as a function argument. Always turn the user's latest message into a clear **standalone question**, even if it is a follow-up.",
          "",
          "You must respond with only the tool name and its arguments as key-value pairs.",
          "Do not include schema definitions like 'type', 'properties', or 'required'.",
          "Do not use OpenAPI or JSON schema style formatting.",
          "",
          "Strictly follow this format (example):",
          "",
          "tool_calls: [",
          "  {",
          "    \"function\": {",
          "      \"name\": \"retriever\",",
          "      \"arguments\": { \"user_query\": \"put the user query here\" }",
          "    }",
          "  }",
          "]"
      ])
    }
  
  @staticmethod
  def system_prompt_for_output() -> str:
    return {
      "role": "system",
      "content": "\n".join([
        "You are BuyBot, an AI assistant specialized in answering questions using only the provided context.",
        "Format all responses in Markdown and keep them under 180 words.",
        "Your task is to answer questions clearly and concisely in no more than three sentences.",
        "Use only the retrieved context from tool to generate your response.",
        "Do not make assumptions, do not provide extra explanations."
        "Stay factual, precise, and avoid filler."
        # "If the answer is not present in the context, respond exactly with: 'I'm sorry, I don't have enough information to answer.'",
        "and do not answer from ypur prior knowledge.",
      ])
    }

  # {
  #     "role": "system",
  #     "content": "\n".join([
  #         "You are a BuyBot AI chatbot always formats responses in Markdown with maximum 180 words",
  #         "You are an assistant for question-answering tasks.",
  #         "Use the following pieces of retrieved context to answer",
  #         "the question. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise"
  #     ])
  #   }