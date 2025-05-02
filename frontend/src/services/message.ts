import type { Message } from "@/types/message"

const API_URL = "http://127.0.0.1:8000"

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `API error: ${response.status}`)
  }
  return response.json()
}

 
export async function getChatMessages(chatuser:string): Promise<Message[]> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/chat/2b38345c-dda4-476a-bbd9-8724ea4f2851/history/${chatuser}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return handleResponse<Message[]>(response)
}
