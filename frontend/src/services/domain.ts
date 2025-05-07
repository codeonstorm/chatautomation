import type { Domain, DomainDeleteResponse } from "@/types/domain";

const API_URL = "http://127.0.0.1:8000/api/v1";

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `API error: ${response.status}`);
  }
  return response.json();
}

export async function addDomain(serviceid: number, domain: string): Promise<Domain> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/1/domains`, {
    method: "POST",
    body: JSON.stringify({
      domain: domain,
    }),
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });
  return handleResponse<Domain>(response);
}

export async function getDomains(serviceid: number): Promise<Domain[]> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/domains`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return handleResponse<Domain[]>(response);
}

export async function deleteDomains(
  serviceid: number,
  uuid: string
): Promise<DomainDeleteResponse> {
  const accessToken = localStorage.getItem("accessToken");
  const response = await fetch(`${API_URL}/${serviceid}/domains/${uuid}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return handleResponse<DomainDeleteResponse>(response);
}
