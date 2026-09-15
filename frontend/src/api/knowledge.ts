import { apiGet, apiPost } from "./client";
import type { KnowledgeStateItem } from "../types/domain";

export function getKnowledgeState() {
  return apiGet<{ items: KnowledgeStateItem[] }>("/knowledge/state");
}

export function resetKnowledgeState() {
  return apiPost<{ status: string; items: KnowledgeStateItem[] }>("/knowledge/reset");
}
