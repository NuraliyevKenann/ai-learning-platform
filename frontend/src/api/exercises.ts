import { apiGet } from "./client";
import type { Exercise } from "../types/domain";

export function getExercises() {
  return apiGet<{ items: Exercise[] }>("/exercises");
}
