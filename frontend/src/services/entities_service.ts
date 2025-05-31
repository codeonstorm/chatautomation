import { Entity } from '@/types/entity'

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

export async function createEntity(serviceid: number, chatbot_uuid: string, entity: any): Promise<Entity> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/entities`, {
    method: "POST",
    body: JSON.stringify(entity),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Entity>(response);
}

export async function getEntity(serviceId: number, chatbotUuid: string, entityid: string): Promise<Entity> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/entities/${entityid}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Entity>(response);
}

export async function getEntities(serviceId: number, chatbotUuid: string): Promise<Entity[]> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/entities`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Entity[]>(response);
}

export async function updateEntity(serviceid: number, chatbot_uuid: string, entityid: string, entity: any): Promise<Entity> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/entities/${entityid}`, {
    method: "PATCH",
    body: JSON.stringify(entity),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Entity>(response);
}

export async function deleteEntity(serviceId: number, chatbotUuid: string, entityId: string): Promise<any> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/entities/${entityId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<any>(response);
}
