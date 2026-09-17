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
  title: string;
  prompt: string;
  difficulty: string;
  estimated_minutes: number;
  hint: string;
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
  feedback: string;
  hint: string | null;
  solution: string | null;
  explanation: string;
  recommendation: Recommendation;
};

export type AttemptHistoryItem = {
  id: number;
  exercise_id: string;
  answer: string;
  is_correct: boolean;
  score: number;
  old_mastery: number;
  new_mastery: number;
  created_at: string;
};

export type User = {
  id: string;
  email: string;
  display_name: string;
  created_at: string;
};

export type AuthResponse = {
  user: User;
};

export type CourseSummary = {
  id: string;
  title: string;
  description: string;
  status: string;
  goal_id: string | null;
  selected: boolean;
  selected_at: string | null;
};

export type CourseListResponse = {
  items: CourseSummary[];
};

export type MyLearningResponse = {
  selected_courses: CourseSummary[];
  active_course: CourseSummary | null;
  available_courses: CourseSummary[];
};
