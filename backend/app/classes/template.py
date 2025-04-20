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
  

  
  @staticmethod
  def system_prompt_for_tools_intro() -> str:
    return {
      "role": "system",
      "content": "\n".join([
          "You are a BuyBot AI chatbot. You must select only one most relevant tool from the provided tools.",
          "Tools Information helps you in selection:",
          "- greeting: Use for replies like: Hi, Hello, Thanks, Bye!",
          "- retriever: Use for questions asking for facts, product info, knowledge, or data from a knowledge base or data store.",
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
          "You are a BuyBot AI chatbot always formats responses in Markdown with maximum 180 words"
      ])
    }