export type Goal = {
  id: string;
  title: string;
  description: string;
};

export type Topic = {
  id: string;
  goal_id: string;
  title: string;
  skill_id: string;
  order: number;
};

export type Exercise = {
  id: string;
  topic_id: string;
  skill_id: string;
  prompt: string;
  difficulty: string;
};

export type KnowledgeStateItem = {
  user_id: string;
  skill_id: string;
  mastery: number;
  level: string;
};

export type Recommendation = {
  type: "start_exercise" | "next_exercise" | "retry_exercise" | "complete_goal";
  exercise_id: string | null;
  reason: string;
};

export type AttemptResult = {
  status: string;
  exercise_id: string;
  is_correct: boolean;
  score: number;
  old_mastery: number;
  new_mastery: number;
  recommendation: Recommendation;
};
