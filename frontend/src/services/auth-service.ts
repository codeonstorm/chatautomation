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

// Login user
export async function login(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("grant_type", "password");
  formData.append("username", email);
  formData.append("password", password);
  formData.append("scope", "");
  formData.append("client_id", "");
  formData.append("client_secret", "");

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json",
    },
    body: formData.toString(),
  });

  return handleResponse<{
    access_token: string;
    refresh_token: string;
    token_type: string;
  }>(response);
}


// Refresh token
export async function refreshToken(refresh_token: string) {
  const response = await fetch(`${API_URL}/auth/refresh`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh_token }),
  })

  return handleResponse<{
    access_token: string
    refresh_token: string
    token_type: string
  }>(response)
}

// Get current user
export async function getCurrentUser(): Promise<User> {
  const accessToken = localStorage.getItem("accessToken")

  const response = await fetch(`${API_URL}/users/user`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  return handleResponse<User>(response)
}

// Create user
export async function createUser(userData: {
  email: string
  name: string
  password: string
}) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...userData,
      // is_active: userData.is_active ?? true,
      // is_superuser: userData.is_superuser ?? false,
    }),
  })

  return handleResponse<User>(response)
}

// Update user
export async function updateUser(
  userId: string,
  userData: Partial<{
    email: string
    full_name: string
    password: string
    is_active: boolean
    is_superuser: boolean
  }>,
) {
  const accessToken = localStorage.getItem("accessToken")

  const response = await fetch(`${API_URL}/users/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(userData),
  })

  return handleResponse<User>(response)
}

