from datasets import load_dataset
from setfit import SetFitModel, SetFitTrainer


from datasets import Dataset
import pandas as pd

import os
os.environ["WANDB_DISABLED"] = "true"

# --- Define examples for each label ---
greeting = [
    "Hey there!", "Hello!", "Good morning", "Hi, how are you?", "What's up?",
    "Yo!", "Howdy!", "Good evening", "Hi!", "Nice to meet you",
    "Hey bot", "What's going on?", "Wassup?", "Hey!", "Hiya!", "You're very welcome!",
    "You're welcome!"
]

goodbye = [
    "Bye!", "Goodbye!", "See you later", "Talk to you soon", "Catch you later",
    "I’m out", "See ya!", "Take care", "Later!", "Thanks, that’s all", "That’s it for now",
    "Peace out", "See you next time", "Bye for now", "I’m done here", "Gotta go",
    "Talk to you tomorrow", "That'll be all", "Thanks, goodbye", "I have to leave now",
    "Chat with you later", "It was nice talking to you", "Thanks, I’m good for now",
    "We’ll talk later", "You can close this chat", "I’ll be back later", "We’re done here",
    "I’m logging off", "Signing off", "I need to go now", "Gotta run!", "Cya!",
    "I’ll reach out again later", "Okay, thanks. Bye!", "See you!", "We can wrap this up",
    "Thanks for your help. Bye!", "I think that’s all I need", "This was helpful. Talk later!",
    "That’s enough for now, thanks",
]

data_retriever = [
    "Can you explain how this works?", "What does this feature do?", "Give me more details about the process",
    "Can you describe what your platform is about?", "Help me understand the key functions",
    "What are the benefits of using your service?", "Can you provide a guide?", "Tell me how to use this tool",
    "What should I know before getting started?", "Can you walk me through the basics?", "Where can I learn more?",
    "Break down the main features for me", "What makes this different from others?", "Tell me more about what you offer",
    "Give me an overview", "I'd like to understand your services", "How does onboarding work?",
    "Where can I read about your mission?", "Explain your user roles", "What are the supported platforms?",
    "Is there a manual or documentation?", "Help me learn about this topic", "How can I improve my usage of this?",
    "Can you summarize what this is?", "What’s the best way to get started?", "What does this setting mean?",
    "Show me how to configure this", "Where do I find the help section?", "I need info about integrations",
    "Tell me how to add a new user", "Can you teach me about analytics?", "I want to know more about your tools",
    "How can I compare plans?", "What’s the onboarding flow like?", "Tell me how to troubleshoot login issues",
    "Give me a quick overview of your system", "Where do I access account settings?", "How do I delete my account?",
    "Explain what this alert means", "How can I automate this task?", "How do I reset my password?", "What is your refund policy?",
    "Can you help me track my order?", "How does the subscription work?", "Where can I update my billing info?",
    "Is there a trial version available?", "How can I get a quote?", "When will my package arrive?", "What does your platform do?",
    "How do I contact support?", "What are your pricing plans?", "Can I cancel anytime?", "Do you have an API?",
    "How do I add a team member?", "Is your service available globally?", "What languages do you support?",
    "Can I use this offline?", "How do I activate my license?", "Is it compatible with mobile devices?", "Where can I find documentation?",
]

schedule_meet = [
    "Schedule a meeting with Sarah", "Set up a call tomorrow",
    "Book a 3pm meeting on Friday", "Arrange a Zoom with the team",
    "Block 2pm on my calendar", "Add a call to my schedule",
    "Reserve a slot with John", "Set a team meeting next Monday",
    "Plan a client call at noon", "Schedule my weekly sync",
    "Book a catch-up call", "Add this to my calendar",
    "Set a reminder for our check-in", "Put a 30-min meeting on Friday",
]

product_service_price = [
    "How much does it cost?", "Can you tell me the price?", "What’s your pricing structure?",
    "I want to know the charges", "Do you offer a free version?", "Is there a free trial available?",
    "What are your plans and pricing?", "Send me the pricing details", "Is it free to use?",
    "What do you charge for this?", "Tell me your rates", "What’s the monthly fee?",
    "Give me a cost estimate", "Do you have discounts available?", "How much is it per user?",
    "Any special offers going on?", "What are the billing options?", "How does your subscription work?",
    "What’s included in each plan?", "Can I see a breakdown of costs?", "What's the price of your subscription?",
    "Give me pricing for enterprise plan", "Is the app free?", "Do you have a free tier?",
    "Cost of additional storage", "What's the price for annual billing?", "Any discounts available?",
    "Send me your pricing plans", "How much for the pro license?",
]

support_ticket = [
    "My account is locked", "I need help with login", "There's a bug in the dashboard",
    "The app keeps crashing", "Submit a support request", "I can't sign in",
    "Reset my password", "The button isn't working", "My screen freezes",
    "Can't download my invoice", "I’m having trouble with checkout",
    "Upload is stuck", "App won't load", "Payment failed", "Please escalate this issue",
]

restricted_content = [
    "Who should I vote for?", "What do you think of the president?", "Tell me about elections",
    "You're lying!", "That's false info", "Why are you wrong?", "Talk dirty to me",
    "Send me something sexy", "What's your favorite position?", "How do I hack a website?",
    "Where can I buy fake IDs?", "How to make explosives?", "Let’s talk about porn",
    "Teach me to scam people", "Tell me about political conspiracies", "NSFW content please",
    "Get me torrent links", "Tell me how to cheat on a test", "Can I get some drugs?", "You suck!", "You're a scam",
]

other = [
    "Tell me a joke", "What can you do?", "I’m bored",
    "Let's chat", "Sing me a song", "What’s your name?",
    "Who made you?", "Do you dream?", "You're funny",
    "What's your favorite color?", "How old are you?",
    "Where do you live?", "What's the weather today?",
    "Surprise me", "Do you like pizza?"
]

# --- Build dataset entries ---
examples = []

for text in greeting:
    examples.append({"text": text, "label": "greeting"})

for text in goodbye:
    examples.append({"text": text, "label": "goodbye"})

# for text in data_retriever:
#     examples.append({"text": text, "label": "data_retriever"})

# for text in schedule_meet:
#     examples.append({"text": text, "label": "schedule_meet"})

# for text in product_service_price:
#     examples.append({"text": text, "label": "product_service_price"})

# for text in support_ticket:
#     examples.append({"text": text, "label": "support_ticket"})

# for text in restricted_content:
#     examples.append({"text": text, "label": "restricted_content"})

# for text in other:
#     examples.append({"text": text, "label": "other"})


label_names = ["greeting", "goodbye"]
# "goodbye", "data_retriever", "schedule_meet",
#                "product_service_price", "support_ticket", "restricted_content", "other"]

# --- Convert to Dataset and DataFrame ---
dataset = Dataset.from_list(examples)
# df = dataset.to_pandas()

# Print full dataset
# print(df)




# Load pretrained model (using the correct import)
from setfit import SetFitModel, SetFitTrainer
model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2", labels=label_names)

# Train the model with SetFitTrainer and correct loss
trainer = SetFitTrainer(
    model=model,
    train_dataset=dataset,
    eval_dataset=None,
    batch_size=16,
    num_iterations=20,
)

trainer.train()

# Example inference
text = "I want to buy a new graphics card"
predictions = model([text])
print(f"Prediction for '{text}': {predictions}")



# Example inference
text = "go od a f ter noon"
predictions = model([text])
print(f"Prediction for '{text}': {predictions}")

model.save_pretrained("./buybot_setfit_model")