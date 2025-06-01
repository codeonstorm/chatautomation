import type {fileMetaType} from "@/types/file"

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
export async function getFileList(serviceid: number, chatbot_uuid: String): Promise<fileMetaType[]> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/filemanager/files`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  return handleResponse<fileMetaType[]>(response)
}

 
 
