import { apiGet, apiPost } from "./client";
import type { AuthResponse, User } from "../types/domain";

export async function register(input: { display_name: string; email: string; password: string }) {
  const response = await apiPost<AuthResponse>("/auth/register", input);
  return response.user;
}

export async function login(input: { email: string; password: string }) {
  const response = await apiPost<AuthResponse>("/auth/login", input);
  return response.user;
}

export function getMe() {
  return apiGet<User>("/auth/me");
}

export async function logout() {
  await apiPost<{ status: string }>("/auth/logout");
}
