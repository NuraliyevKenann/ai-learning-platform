import { apiGet, apiPost, clearAuthToken, saveAuthToken } from "./client";
import type { AuthResponse, User } from "../types/domain";

export async function register(input: { display_name: string; email: string; password: string }) {
  const response = await apiPost<AuthResponse>("/auth/register", input);
  saveAuthToken(response.access_token);
  return response.user;
}

export async function login(input: { email: string; password: string }) {
  const response = await apiPost<AuthResponse>("/auth/login", input);
  saveAuthToken(response.access_token);
  return response.user;
}

export function getMe() {
  return apiGet<User>("/auth/me");
}

export async function logout() {
  try {
    await apiPost<{ status: string }>("/auth/logout");
  } finally {
    clearAuthToken();
  }
}
