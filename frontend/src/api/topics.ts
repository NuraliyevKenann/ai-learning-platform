import { apiGet } from "./client";
import type { Topic } from "../types/domain";

export function getTopics() {
  return apiGet<{ items: Topic[] }>("/topics");
}
