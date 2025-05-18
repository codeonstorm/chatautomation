import { Webhook, StatusEnum, WebhookState } from '@/types/webhook'

const API_URL = "http://127.0.0.1:8000/api/v1";

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }
  return response.json();
}

// Webhook API calls

export async function createWebhook(serviceid: number, chatbot_uuid: string, webhook: any): Promise<Webhook> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/webhook`, {
    method: "POST",
    body: JSON.stringify(webhook),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Webhook>(response);
}

export async function getWebhook(serviceId: number, chatbotUuid: string): Promise<Webhook> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/webhook`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Webhook>(response);
}

export async function updateWebhook(serviceid: number, chatbot_uuid: string, webhook: any): Promise<Webhook> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/${chatbot_uuid}/webhook`, {
    method: "PATCH",
    body: JSON.stringify(webhook),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Webhook>(response);
}

export async function deleteWebhook(serviceId: number, chatbotUuid: string, webhookId: string): Promise<any> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceId}/${chatbotUuid}/webhook`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<any>(response);
}
