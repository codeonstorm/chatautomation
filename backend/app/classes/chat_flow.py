from app.schemas.context_store import ContextStore
from app.classes.greeting import GreetingResponder
from app.classes.ner.regex_ner_extractor import RegexNERExtractor
from app.classes.ner.synonym_ner_extractor import SynonymNERExtractor

from app.classes.template import Template
from ollama import ChatResponse, chat, ResponseError, Client

from app.classes.base_tool import BaseTool

import time
import requests

class ChatFlow:

    def __init__(self, setfit_model, intentsList, entitiesList, webhook_config):
        self.chat_history_store = []
        self.context_store = ContextStore(intent='', context='', slots={})
        self.entitiesList = entitiesList
        self.intentsList = intentsList
        self.setfit_model = setfit_model
        self.webhook_config = webhook_config
        print("*************** ChatFlow Initialized **********")


    def chat(self, query: str):
        print("\n\n\n===== query: ", query, " =====")
        print("storage: ", self.context_store)
        if len(query) < 2:
            return "Please provide a more detailed."

        responder = GreetingResponder()
        response = responder.check_greeting(query)
        if response:
            return response

        try:
            triggered_intent = self.get_intent_detail(query)
            reply = self.perform_action_for_intent(triggered_intent, query)
            if reply: return reply
            return self.llm_response(query)
        except ResponseError as e:
            return f"Error in chat processing: {e}"
        
    
    def get_intent_detail(self, query):
        predicted_intent = self.setfit_model([query])
        print(f"SetFitModel Intent ': {predicted_intent}")
        if predicted_intent[0] == 'other':
            predicted_intent = None

        if not predicted_intent and self.context_store.intent and self.context_store.slots: #
            predicted_intent = [self.context_store.intent] # 
        print(f"override intent ': {predicted_intent}")
        
        return self.intentsList.get(predicted_intent[0], None)
    


    def perform_action_for_intent(self, triggered_intent, query):
        if not triggered_intent or not triggered_intent.action:
            return None

        action_arguments = triggered_intent.action.parameters
        entities = RegexNERExtractor.extract_entities(text=query)
        print("RegexNERExtractor entities: ", entities, end="\n")

        if not self.context_store.slots:
            self.context_store.slots = entities
        else:
            for entity in self.context_store.slots:
                self.context_store.slots[entity] = (self.context_store.slots.get(entity) or []) + (entities.get(entity) or [])

        # slot filling ..
        self.context_store = ContextStore(
            intent="schedule_meet",
            context="appointment",
            slots= self.context_store.slots
        )

        print("updated storage:", self.context_store, "\n")
        print("action_arguments=>:", action_arguments, "\n")

        if self.context_store and self.context_store.slots:
            for args in action_arguments:
                if args.required:
                    if not len(self.context_store.slots.get(args.parameter) or []):
                        return args.message
                    
        # flush store context
        self.context_store = ContextStore(
            intent='',
            context='',
            slots={}
        )

        if triggered_intent.action.webhook == True:
            # call_webhook = self.call_webhook(
            #     self.webhook_config,
            #     data={
            #         "query": "https://example.com/api",
            #         "entities": [],
            #         "context_store": self.context_store.dict() if self.context_store else {},
            #     },
            # )
            return "webhook called"
        
        if action_arguments.default_intent_responses:
            return action_arguments.default_intent_responses[0]
        return None



    def call_webhook(self, webhook_config: dict, data: dict):
        url = webhook_config.get("endpoint")
        if not url:
            print("Webhook endpoint URL is missing.")
            return None

        # Start with any headers provided in 'header' field
        headers = webhook_config.get("header", {}).copy()

        # Dynamically add x-api-key or any keys from 'basic_auth'
        basic_auth = webhook_config.get("basic_auth", {})
        for key, value in basic_auth.items():
            headers[key] = value

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.text  # or response.text
        except requests.exceptions.RequestException as e:
            print(f"Error calling webhook: {e}")
            return None

    

    def standalone_question(self, query: str):
        stand = [Template.condense_question_system_template()]
        for history in self.chat_history_store:
            stand.append(history)
        stand.append({"role": "user", "content": query})

        t2 = time.time()
        standalone_response: ChatResponse = chat(
            "gemma3:1b",
            # "llama3.2:1b-instruct-q3_K_L",
            keep_alive="60m",
            messages=stand,
        )
        standalone_question = standalone_response.message.content
        print(
            "\ngemma3:1b standalone Que: ",
            standalone_question,
            time.time() - t2,
            "seconds",
        )
        return standalone_question
    

    
    def llm_response(self, query: str):
        # Standalone Question Preparation
        standalone_question = self.standalone_question(query)
        # Update chat history with the standalone question
        user_message = {"role": "user", "content": standalone_question}
        self.chat_history_store.append({
            "role": "user",
            "content": query,
        })

        # Get final response
        t3 = time.time()
        tool_response = BaseTool.retriever(standalone_question)
        print("\n===Tool response time:", time.time() - t3, "seconds\n")
        print("Tool response:\n", tool_response, end="\n\n")
        tool_message = {
            "role": "tool",
            "name": "retriever",
            "content": str(tool_response),
        }
        messages = [Template.system_prompt_for_output(), tool_message, user_message]

        final_response = chat(
            "llama3.2:1b-instruct-q3_K_L",
            messages=messages,
            keep_alive="60m",
        )
        self.chat_history_store.append({
            "role": "assistant",
            "content": final_response.message.content,
        })

        if not final_response.message.content:
            return "'I'm sorry, I don't have enough information."

        return f"{final_response.message.content}"
