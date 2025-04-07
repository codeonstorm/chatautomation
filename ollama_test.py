# from ollama import chat

# messages = [
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
#   {
#     'role': 'assistant',
#     'content': "The sky is blue because of the way the Earth's atmosphere scatters sunlight.",
#   },
#   {
#     'role': 'user',
#     'content': 'What is the weather in Tokyo?',
#   },
#   {
#     'role': 'assistant',
#     'content': 'The weather in Tokyo is typically warm and humid during the summer months, with temperatures often exceeding 30°C (86°F). The city experiences a rainy season from June to September, with heavy rainfall and occasional typhoons. Winter is mild, with temperatures rarely dropping below freezing. The city is known for its high-tech and vibrant culture, with many popular tourist attractions such as the Tokyo Tower, Senso-ji Temple, and the bustling Shibuya district.',
#   },
# ]

# while True:
#   user_input = input('Chat with history: ')
#   response = chat(
#     'llama3.2',
#     messages=messages
#     + [
#       {'role': 'user', 'content': user_input},
#     ],
#     stream=True
#   )
#   for part in response:
#     print(part['message']['content'], end='')

#   print(response)

#   # Add the response to the messages to maintain the history
#   # messages += [
#   #   {'role': 'user', 'content': user_input},
#   #   {'role': 'assistant', 'content': response.message.content},
#   # ]
#   # print(response.message.content + '\n')


# from ollama import embed

# response = embed(model='llama3.2', input='Hello, world!')
# print(response['embeddings'])

# from ollama import ProcessResponse, chat, ps, pull

# # Ensure at least one model is loaded
# response = pull('llama3.2', stream=True)
# progress_states = set()
# for progress in response:
#   if progress.get('status') in progress_states:
#     continue
#   progress_states.add(progress.get('status'))
#   print(progress.get('status'))

# print('\n')

# print('Waiting for model to load... \n')
# chat(model='llama3.2', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])


# response: ProcessResponse = ps()
# for model in response.models:
#   print('Model: ', model.model)
#   print('  Digest: ', model.digest)
#   print('  Expires at: ', model.expires_at)
#   print('  Size: ', model.size)
#   print('  Size vram: ', model.size_vram)
#   print('  Details: ', model.details)
#   print('  Details: ', model)
#   print('\n')

from ollama import ChatResponse, chat


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
      a (int): The first number
      b (int): The second number

    Returns:
      int: The sum of the two numbers
    """

    # The cast is necessary as returned tool call arguments don't always conform exactly to schema
    # E.g. this would prevent "what is 30 + 12" to produce '3012' instead of 42
    return int(a) + int(b)


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """

    # The cast is necessary as returned tool call arguments don't always conform exactly to schema
    return int(a) - int(b)


# Tools can still be manually defined and passed into chat
subtract_two_numbers_tool = {
    "type": "function",
    "function": {
        "name": "subtract_two_numbers",
        "description": "Subtract two numbers",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": "The first number"},
                "b": {"type": "integer", "description": "The second number"},
            },
        },
    },
}

messages = [{"role": "user", "content": "What is three plus one?"}]
print("Prompt:", messages[0]["content"])

available_functions = {
    "add_two_numbers": add_two_numbers,
    "subtract_two_numbers": subtract_two_numbers,
}

response: ChatResponse = chat(
    "llama3.2",
    messages=messages,
    tools=[add_two_numbers, subtract_two_numbers_tool],
)

if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
            print("Calling function:", tool.function.name)
            print("Arguments:", tool.function.arguments)
            output = function_to_call(**tool.function.arguments)
            print("Function output:", output)
        else:
            print("Function", tool.function.name, "not found")

# Only needed to chat with the model using the tool call results
if response.message.tool_calls:
    # Add the function response to messages for the model to use
    messages.append(response.message)
    messages.append(
        {"role": "tool", "content": str(output), "name": tool.function.name}
    )

    # Get final response from model with function outputs
    final_response = chat("llama3.2", messages=messages)
    print("Final response:", final_response.message.content)

else:
    print("No tool calls returned from model")
