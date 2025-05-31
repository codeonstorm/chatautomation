import { Intent } from '@/types/intent'

const API_URL = "http://127.0.0.1:8000/api/v1";

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }
  return response.json();
}

// Entity API calls

export async function createIntent(serviceid: number, chatbot_uuid: string, intent: any): Promise<Intent> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/intents`, {
    method: "POST",
    body: JSON.stringify(intent),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Intent>(response);
}

export async function getIntent(serviceId: number, chatbotUuid: string, intentid: string): Promise<Intent> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/intents/${intentid}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Intent>(response);
}

export async function getIntents(serviceId: number, chatbotUuid: string): Promise<Intent[]> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/intents`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Intent[]>(response);
}

export async function updateIntent(serviceid: number, chatbot_uuid: string, intentid: string, intent: any): Promise<Intent> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/intents/${intentid}`, {
    method: "PATCH",
    body: JSON.stringify(intent),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Intent>(response);
}

export async function deleteIntent(serviceId: number, chatbotUuid: string, intentid: string): Promise<any> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/intents/${intentid}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<any>(response);
}
