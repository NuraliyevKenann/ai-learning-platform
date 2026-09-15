import { apiPost } from "./client";
import type { AttemptResult } from "../types/domain";

export type SubmitAttemptInput = {
  exercise_id: string;
  answer: string;
};

export async function submitAttempt(input: SubmitAttemptInput) {
  return apiPost<AttemptResult>("/attempts", input);
}
