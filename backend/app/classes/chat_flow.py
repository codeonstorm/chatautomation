from app.schemas.context_store import ContextStore
from app.classes.greeting import GreetingResponder
from app.classes.ner.regex_ner_extractor import RegexNERExtractor
from app.classes.ner.synonym_ner_extractor import SynonymNERExtractor

from app.classes.template import Template
from ollama import ChatResponse, chat, ResponseError, Client

from app.classes.base_tool import BaseTool

import time


class ChatFlow:

    def __init__(self, setfit_model, intentsList, entitiesList):
        self.chat_history_store = []
        self.context_store: ContextStore | None = None
        self.entitiesList = entitiesList
        self.intentsList = intentsList

        self.setfit_model = setfit_model
        print("*************** ChatFlow Initialized **********")

    def chat(self, query: str):
        if self.context_store is not None:
            print(
                "======>>>>context",
                self.context_store.intent,
                self.context_store.context,
                self.context_store.slots,
            )

        if len(query) < 2:
            return "Please provide a more detailed."

        responder = GreetingResponder()
        response = responder.check_greeting(query)
        if response:
            return response

        try:
            t1 = time.time()
            predicted_intent = self.setfit_model([query])
            #  slot filling
            print(
                f"\n\n\n\nSetFitModel Intent ': {predicted_intent} {time.time() - t1} seconds"
            )


            if predicted_intent == "other":
                if self.context_store:
                    predicted_intent = self.context_store.intent
            print("\n\n\n\nUsing context store intent: ", predicted_intent)

            if predicted_intent == "greeting":
                return "Hello! How can I help you today?"

            elif predicted_intent == "goodbye":
                return "Take care, until next time!"

            elif predicted_intent == "restricted_content":
                return "I'm here to help with respectful, safe, and appropriate topics. Let's keep things positive and productive!"

            elif predicted_intent == "schedule_meet":
                # set store
                #  set intent, context, entity w/ value
                # check actions

                # check entities
                action_arguments = {
                    "email": {
                        "required": True,
                        "msg": "Please provide email to schedule meet",
                    },
                    "mobile": {
                        "required": True,
                        "msg": "Mobile number required to schedule meet",
                    },
                    "date": {
                        "required": True,
                        "msg": "Please provide date for the appointment",
                    },
                    "time": {
                        "required": True,
                        "msg": "Please provide time for the appointment",
                    },
                }
                entities = RegexNERExtractor.extract_entities(text=query)
                print("\n\n\n\nRegexNERExtractor entities: ", entities, end="\n\n")

                self.context_store = ContextStore(
                    intent="schedule_meet",
                    context="appointment",
                    slots=self.context_store.slots,
                )

                # for entity, value in entities.items():
                #     if entity not in self.context_store.slots:
                #         self.context_store.slots[entity] = []

                #     # Append only if value is not None or empty
                #     if value:
                #         self.context_store.slots[entity].append(value)

                for arg, arg_props in action_arguments.items():
                    if arg_props.get("required", False):
                        if not entities.get(
                            arg
                        ):  # Checks for None, empty string, or empty list
                            if self.context_store.slots is not None:
                                continue
                            return arg_props.get(
                                "msg", "Please provide the required information."
                            )

                    # check if webhook enabled

                    # default response
                return "Sorry, Meet scheduling is not available at the moment."

            # Standalone Question Preparation
            stand = [Template.condense_question_system_template()]
            for history in self.chat_history_store:
                stand.append(history)
            stand.append({"role": "user", "content": query})
            # print('\n\n stand: ', stand)

            t2 = time.time()
            standalone_response: ChatResponse = chat(
                "gemma3:1b",
                # "llama3.2:1b-instruct-q3_K_L",
                keep_alive="60m",
                messages=stand,
            )
            standalone_question = standalone_response.message.content
            print(
                "\ngemma3:1b stanalone Que: ",
                standalone_question,
                time.time() - t2,
                "seconds",
            )

        except ResponseError as e:
            print("Error:", e.error)
            # await manager.send_personal_message("Error...", websocket)
            # continue

        # Update chat history with the standalone question
        user_message = {"role": "user", "content": standalone_question}
        self.chat_history_store.append(
            {
                "role": "user",
                "content": query,
            }
        )

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
        try:
            t4 = time.time()
            final_response = chat(
                "llama3.2:1b-instruct-q3_K_L",
                messages=messages,
                keep_alive="60m",
            )
            print("===LLAMA response time:", time.time() - t4, "seconds")

            self.chat_history_store.append(
                {
                    "role": "assistant",
                    "content": final_response.message.content,
                }
            )
        except ResponseError as e:
            print("Error:", e.error)
            # await manager.send_personal_message("Error...S", websocket)
            # continue

        # print("\n\n\n history:", chat_history_store)
        # print("\n\nFinal response:\n", final_response.message.content)

        # for chunk in final_response:
        #   await websocket.send_text(f"{chunk['message']['content']}")
        #   print(chunk['message']['content'], end='', flush=True)

        # end_time = time.time()
        # elapsed_time = end_time - start_time
        return f"{final_response.message.content} **time taken: {round(time.time() - t1)} seconds**"
