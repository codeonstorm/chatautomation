import type { Chatbot } from "@/types/chatbot"

const API_URL = "http://127.0.0.1:8000/api/v1"

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `API error: ${response.status}`)
  }
  return response.json()
}

export async function getChatbots(): Promise<Chatbot[]> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/1/chatbots`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  })
  return handleResponse<Chatbot[]>(response)
}
 

export async function createChatbot(chatbot: Chatbot): Promise<Chatbot> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/1/chatbots`, {
    method: "POST",
    body: JSON.stringify({
      ...chatbot
    }),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  })
  return handleResponse<Chatbot>(response)
}

export async function updateChatbot(chatbot: Chatbot): Promise<Chatbot> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/1/chatbots/${chatbot.uuid}`, {
    method: "PATCH",
    body: JSON.stringify({
      ...chatbot
    }),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  })
  return handleResponse<Chatbot>(response)
}

export async function deleteChatbot(uuid: string): Promise<any> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/1/chatbots/${uuid}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  })
  return handleResponse<any>(response)
}
 