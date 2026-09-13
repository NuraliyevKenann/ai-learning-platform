import { apiGet } from "./client";
import type { Recommendation } from "../types/domain";

export function getCurrentRecommendation() {
  return apiGet<{ recommendation: Recommendation | null }>("/recommendations/current");
}
