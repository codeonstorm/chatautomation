import type { ChatUser } from "@/types/chatuser"

const API_URL = "http://127.0.0.1:8000"

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `API error: ${response.status}`)
  }
  return response.json()
}

 
export async function getChatUsers(id: string): Promise<ChatUser[]> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/chat/${id}/users`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return handleResponse<ChatUser[]>(response)
}
