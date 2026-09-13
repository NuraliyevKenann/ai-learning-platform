import { apiGet } from "./client";
import type { Goal } from "../types/domain";

export function getGoals() {
  return apiGet<{ items: Goal[] }>("/goals");
}
