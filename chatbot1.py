from ollama import ChatResponse, chat, ResponseError
from src.classes.QdrantManager import QdrantManager

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import time

app = FastAPI()

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

def greeting(query: str) -> int:
  """
  tool for greeting query **only. example: Hi, Hello, Hey, Thanks, bye, OK, Good Morning, Good Evning.
    Args:
        query (str): The query
  Returns:
    (str): The result of the query
  """
  return query
 
def retrive_data_for_aggregation(query: str) -> str:
  """
  tool to get updated information based on the given query.
  Args:
    query (str): The query string to search for relevant documents.
  Returns:
    (str): A list of dictionaries containing retrieved documents.
  """
  try:
    qdrant_manager = QdrantManager()
    vector_store = qdrant_manager.get_vector_store("chatbot")
    retrieved_docs = vector_store.similarity_search(query, k=2)
    return retrieved_docs
  except Exception as e:
    return f"Opps! Error during retrieving data {e}"
    
available_functions = {
  # 'greeting': greeting,
  # 'add_two_numbers': add_two_numbers,
  # 'subtract_two_numbers': subtract_two_numbers,
  'retrive_data_for_aggregation': retrive_data_for_aggregation
}


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
              var messages = document.getElementById('messages'); // Parent container
            var currentMessage = document.createElement('li'); // Create a single message element
            messages.appendChild(currentMessage); // Add to the list
            ws.onmessage = function(event) {
              currentMessage.innerHTML += marked.parse(event.data);

              /*message.innerHTML = marked.parse(event.data); // Convert Markdown to HTML and set it*/
              
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
  return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
    start_time = time.time()
    data = await websocket.receive_text()
    await websocket.send_text(f"{data}")
    
    # User message
    system_prompt = {"role": "system", "content": "You are an AI chatbot always formats responses in Markdown with maximum 120 words"}
    user_message = {'role': 'user', 'content': data}
    print('Prompt:', user_message['content'])

    # Prepare messages
    messages = [system_prompt, user_message]

    # Call the model with tools
    try:
      response: ChatResponse = chat(
      'llama3.2:1b-instruct-q6_K',
      messages=messages,
        tools=[retrive_data_for_aggregation],  
        # tools=[greeting, add_two_numbers, subtract_two_numbers, retrive_data_for_aggregation],  
      )
    except ResponseError as e:
      print('Error:', e.error)


    # print('Selected:', response)
    if response.message.tool_calls:
      tool_outputs = []
      for tool_call in response.message.tool_calls:
        function_name = tool_call.function.name
        function_args = tool_call.function.arguments
        # function_args = {k: int(v) for k, v in function_args.items()}

        if function_to_call := available_functions.get(function_name):
          print('\n\n == Calling function: ==', function_name, 'Arguments:', function_args, end='\n\n')
          
          if function_name != 'greeting':
            # if function_name != 'retrive_data_for_aggregation':
            result = function_to_call(**function_args)
            print('\n\nFunction output:', result, end='\n\n')
            tool_outputs.append({
              'role': 'tool',
              'name': function_name,
              'content': str(result)
            })

      if tool_outputs:
        # Append tool outputs correctly
        messages.extend(tool_outputs)
        # Explicitly instruct the model to respond based on the tool results
        # messages.append({'role': 'user', 'content': 'What is the final answer?'})
        # messages.append({'role': 'system', 'content': "Use the provided context of information to answer the question."})
        # messages.append({"role": "system", "content": "You are an AI chatbot always formats responses in Markdown."})

      print('\n\n **Final Messages:\n', messages, end='\n\n')

      # Get final response
      try:
        final_response = chat('llama3.2:1b-instruct-q6_K', messages=messages)
      except ResponseError as e:
        print('Error:', e.error)

      print('\n\nFinal response:\n', final_response.message.content)

      # for chunk in final_response:
      #   await websocket.send_text(f"{chunk['message']['content']}")
      #   print(chunk['message']['content'], end='', flush=True)
    
      end_time = time.time()
      elapsed_time = end_time - start_time
      await websocket.send_text(f"{final_response.message.content} time:{elapsed_time}")