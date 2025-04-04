import type { User } from "@/types/user"

const API_URL = "http://127.0.0.1:8000/api/v1"

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `API error: ${response.status}`)
  }
  return response.json()
}
 
// Get current user
export async function getFileList(): Promise<User> {
  const accessToken = localStorage.getItem("accessToken")

  const response = await fetch(`${API_URL}/1/filemanager/files`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  return handleResponse<User>(response)
}

 
 
