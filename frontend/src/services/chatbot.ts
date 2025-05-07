import type { Chatbot } from "@/types/chatbot";

const API_URL = "http://127.0.0.1:8000/api/v1";

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }
  return response.json();
}

export async function getChatbots(serviceid: number): Promise<Chatbot[]> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/chatbots`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Chatbot[]>(response);
}

export async function getChatbot(serviceid: number, Chatbot_uuid: string): Promise<Chatbot> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/chatbots/${Chatbot_uuid}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Chatbot>(response);
}


export async function createChatbot(chatbot: Chatbot): Promise<Chatbot> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${chatbot.service_id}/chatbots`, {
    method: "POST",
    body: JSON.stringify({
      ...chatbot,
    }),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Chatbot>(response);
}

export async function updateChatbot(chatbot: Chatbot): Promise<Chatbot> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(
    `${API_URL}/${chatbot.service_id}/chatbots/${chatbot.uuid}`,
    {
      method: "PATCH",
      body: JSON.stringify({
        ...chatbot,
      }),
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    }
  );
  return handleResponse<Chatbot>(response);
}

export async function deleteChatbot(
  serviceid: number,
  uuid: string
): Promise<any> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/chatbots/${uuid}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<any>(response);
}
