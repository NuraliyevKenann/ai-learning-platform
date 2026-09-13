export type Goal = {
  id: string;
  title: string;
  description?: string;
};

export type Skill = {
  id: string;
  title: string;
};

export type Topic = {
  id: string;
  title: string;
  skillIds: string[];
};

export type Exercise = {
  id: string;
  prompt: string;
  type: "multiple_choice" | "short_text" | "code";
  skillIds: string[];
  difficulty: "easy" | "medium" | "hard";
};

export type KnowledgeState = {
  skillId: string;
  masteryScore: number;
  confidence: number;
  evidenceCount: number;
};

export type Recommendation = {
  id: string;
  type: "topic" | "exercise" | "review";
  reason: string;
  targetId: string;
};
