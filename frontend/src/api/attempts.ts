import { apiGet, apiPost } from "./client";
import type { AttemptHistoryItem, AttemptResult } from "../types/domain";

export type SubmitAttemptInput = {
  exercise_id: string;
  answer: string;
};

export async function submitAttempt(input: SubmitAttemptInput) {
  return apiPost<AttemptResult>("/attempts", input);
}

export async function getAttemptHistory() {
  return apiGet<{ items: AttemptHistoryItem[] }>("/attempts/history");
}
