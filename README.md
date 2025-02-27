# chatautomation

conda create --name chatautomation python=3.12
conda activate chatautomation
conda deactivate

pip freeze > requirements.txt
pip install langgraph langchain_community
pip install langchain-ollama langchain-qdrant
pip install python-dotenv
pip install fastapi uvicorn
pip install qdrant_client langchain-core
# URL Loder
pip install --upgrade --quiet unstructured
pip install IPython
pip install WebSocket


# Start Qdrant
docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant



# Next release:
Selenium URL Loader:
Using Selenium allows us to load pages that require JavaScript to render.



for chatroom
# pip install python-jose[cryptography] passlib
# pip install bcrypt


1️⃣ python-jose[cryptography]
Purpose: Handles JWT authentication (JSON Web Tokens) to secure WebSocket communication.

jose (JavaScript Object Signing and Encryption) is a lightweight library to create and verify JWTs.
The [cryptography] part is an extra dependency that ensures secure signing and verification of JWTs.
💡 Why?

Ensures that only authenticated users can access chat.
Prevents unauthorized access to WebSocket endpoints.
Uses secure algorithms (e.g., HS256, RS256) for token signing.
2️⃣ passlib
Purpose: Handles password hashing securely.

Why not store plain text passwords? → That would be a security risk!
passlib provides bcrypt, a strong hashing algorithm used to store passwords securely.
💡 Why?

Prevents password leaks from exposing raw passwords.
bcrypt automatically adds a salt to protect against rainbow table attacks.
Hashes passwords securely so that even if a database is compromised, the passwords remain safe.



uvicorn chatbot1:app --reload
