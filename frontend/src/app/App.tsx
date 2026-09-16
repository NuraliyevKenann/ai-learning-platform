import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight, BookOpen, Check, ChevronRight, CircleHelp, Flame,
  LayoutDashboard, LoaderCircle, LogOut, Menu, RefreshCw, RotateCcw,
  Route, Send, Sparkles, Target, X, XCircle,
} from "lucide-react";

import { getMe, logout } from "../api/auth";
import { submitAttempt } from "../api/attempts";
import { clearAuthToken, getAuthToken } from "../api/client";
import { getExercises } from "../api/exercises";
import { getGoals } from "../api/goals";
import { getKnowledgeState, resetKnowledgeState } from "../api/knowledge";
import { getCurrentRecommendation } from "../api/recommendations";
import { getTopics } from "../api/topics";
import { AuthScreen } from "../components/AuthScreen";
import type { AttemptResult, Exercise, Goal, KnowledgeStateItem, Recommendation, Topic, User } from "../types/domain";

type DashboardData = {
  goals: Goal[];
  topics: Topic[];
  exercises: Exercise[];
  knowledge: KnowledgeStateItem[];
  recommendation: Recommendation | null;
};

const emptyData: DashboardData = { goals: [], topics: [], exercises: [], knowledge: [], recommendation: null };
const skillNames: Record<string, string> = {
  skill_python_variables: "Переменные Python",
  skill_fastapi_routes: "Маршруты FastAPI",
};

function getSkillName(skillId: string) {
  return skillNames[skillId] ?? skillId.replace(/^skill_/, "").replaceAll("_", " ");
}

function getLevelLabel(level: string) {
  return ({ weak: "Нужно изучить", practicing: "В процессе", strong: "Освоено" } as Record<string, string>)[level] ?? level;
}

function getRecommendationTitle(type?: Recommendation["type"]) {
  if (type === "retry_exercise") return "Попробуйте ещё раз";
  if (type === "next_exercise") return "Следующий шаг готов";
  if (type === "complete_goal") return "Цель достигнута";
  return "Начните с основ";
}

function getInitials(name: string) {
  return name.split(" ").slice(0, 2).map((part) => part[0]).join("").toUpperCase();
}

export function App() {
  const [user, setUser] = useState<User | null>(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [data, setData] = useState<DashboardData>(emptyData);
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [resetting, setResetting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  async function loadDashboard() {
    setLoading(true);
    setError(null);
    try {
      const [goals, topics, exercises, knowledge, recommendation] = await Promise.all([
        getGoals(), getTopics(), getExercises(), getKnowledgeState(), getCurrentRecommendation(),
      ]);
      setData({
        goals: goals.items,
        topics: topics.items,
        exercises: exercises.items,
        knowledge: knowledge.items,
        recommendation: recommendation.recommendation,
      });
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Не удалось загрузить данные");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!getAuthToken()) {
      setAuthLoading(false);
      return;
    }
    void getMe()
      .then(setUser)
      .catch(() => clearAuthToken())
      .finally(() => setAuthLoading(false));
  }, []);

  useEffect(() => {
    if (user) void loadDashboard();
  }, [user?.id]);

  const currentExercise = useMemo(() => {
    const recommendedId = data.recommendation?.exercise_id;
    return data.exercises.find((exercise) => exercise.id === recommendedId) ?? data.exercises[0];
  }, [data.exercises, data.recommendation]);

  const currentTopic = data.topics.find((topic) => topic.id === currentExercise?.topic_id);
  const averageMastery = data.knowledge.length
    ? Math.round(data.knowledge.reduce((sum, item) => sum + item.mastery, 0) / data.knowledge.length)
    : 0;
  const completedSkills = data.knowledge.filter((item) => item.mastery >= 70).length;

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!currentExercise || !answer.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      const attempt = await submitAttempt({ exercise_id: currentExercise.id, answer: answer.trim() });
      const knowledge = await getKnowledgeState();
      setResult(attempt);
      setData((current) => ({ ...current, knowledge: knowledge.items, recommendation: attempt.recommendation }));
      if (attempt.is_correct) setAnswer("");
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Не удалось проверить ответ");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleReset() {
    setResetting(true);
    setError(null);
    try {
      const reset = await resetKnowledgeState();
      const recommendation = await getCurrentRecommendation();
      setData((current) => ({ ...current, knowledge: reset.items, recommendation: recommendation.recommendation }));
      setAnswer("");
      setResult(null);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Не удалось сбросить прогресс");
    } finally {
      setResetting(false);
    }
  }

  function moveToRecommendation() {
    setResult(null);
    setAnswer("");
    document.querySelector(".exercise-card")?.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  async function handleLogout() {
    await logout();
    setUser(null);
    setData(emptyData);
    setResult(null);
    setAnswer("");
  }

  if (authLoading) {
    return <div className="auth-loading"><div className="brand__mark"><Sparkles size={20} /></div><LoaderCircle className="spin" size={24} /></div>;
  }

  if (!user) {
    return <AuthScreen onAuthenticated={setUser} />;
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "sidebar--open" : ""}`}>
        <div className="brand">
          <div className="brand__mark"><Sparkles size={20} strokeWidth={2.2} /></div>
          <span>skillway</span>
          <button className="icon-button sidebar__close" onClick={() => setSidebarOpen(false)} aria-label="Закрыть меню"><X size={20} /></button>
        </div>
        <nav className="main-nav" aria-label="Главная навигация">
          <p className="nav-label">Обучение</p>
          <a className="nav-link nav-link--active" href="#dashboard"><LayoutDashboard size={19} /> Дэшборд</a>
          <a className="nav-link" href="#exercise"><BookOpen size={19} /> Практика <span className="nav-count">{data.exercises.length}</span></a>
          <a className="nav-link" href="#path"><Route size={19} /> Учебный путь</a>
          <a className="nav-link" href="#progress"><Target size={19} /> Мой прогресс</a>
        </nav>
        <div className="sidebar__support">
          <a className="nav-link" href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer"><CircleHelp size={19} /> API документация</a>
        </div>
        <div className="profile-card">
          <div className="avatar">{getInitials(user.display_name)}</div>
          <div><strong>{user.display_name}</strong><span>{user.email}</span></div>
          <button className="profile-logout" onClick={() => void handleLogout()} aria-label="Выйти из аккаунта" title="Выйти"><LogOut size={18} /></button>
        </div>
      </aside>
      {sidebarOpen && <button className="sidebar-backdrop" onClick={() => setSidebarOpen(false)} aria-label="Закрыть меню" />}

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <button className="icon-button menu-button" onClick={() => setSidebarOpen(true)} aria-label="Открыть меню"><Menu size={22} /></button>
          <div><p className="eyebrow">Ваше обучение</p><h1>С возвращением!</h1></div>
          <div className="topbar__actions">
            <div className="streak"><Flame size={17} fill="currentColor" /> 3 дня подряд</div>
            <button className="icon-button" onClick={() => void loadDashboard()} aria-label="Обновить данные" title="Обновить"><RefreshCw size={19} /></button>
          </div>
        </header>

        {error && <div className="error-banner" role="alert"><XCircle size={19} /><span>{error}. Проверьте, что backend запущен на порту 8000.</span><button onClick={() => void loadDashboard()}>Повторить</button></div>}

        {loading ? (
          <div className="loading-state"><LoaderCircle className="spin" size={28} /> Загружаем ваш учебный план…</div>
        ) : (
          <>
            <section className="welcome-card">
              <div>
                <span className="status-pill"><span /> Активная цель</span>
                <h2>{data.goals[0]?.title ?? "Python Backend Developer"}</h2>
                <p>{data.goals[0]?.description ?? "Учитесь через короткие практические задания."}</p>
              </div>
              <div className="goal-progress">
                <div className="goal-progress__ring" style={{ "--progress": `${averageMastery * 3.6}deg` } as React.CSSProperties}><div><strong>{averageMastery}%</strong><span>освоено</span></div></div>
                <p>{completedSkills} из {data.knowledge.length} навыков завершено</p>
              </div>
            </section>

            <section className="stats-grid" id="progress" aria-label="Статистика обучения">
              <article className="stat-card"><div className="stat-icon stat-icon--blue"><Target size={20} /></div><div><span>Общий прогресс</span><strong>{averageMastery}%</strong></div><span className="stat-trend">по навыкам</span></article>
              <article className="stat-card"><div className="stat-icon stat-icon--mint"><Check size={20} /></div><div><span>Освоено навыков</span><strong>{completedSkills}</strong></div><span className="stat-trend">из {data.knowledge.length}</span></article>
              <article className="stat-card"><div className="stat-icon stat-icon--orange"><BookOpen size={20} /></div><div><span>Доступно заданий</span><strong>{data.exercises.length}</strong></div><span className="stat-trend">MVP курс</span></article>
            </section>

            <div className="dashboard-grid">
              <section className="exercise-card" id="exercise">
                <div className="section-heading"><div><span className="section-kicker">Рекомендовано сейчас</span><h2>{currentTopic?.title ?? "Текущее упражнение"}</h2></div><span className="difficulty">Начальный</span></div>
                {currentExercise ? (
                  <form onSubmit={handleSubmit}>
                    <div className="exercise-meta"><span>Задание {Math.max(1, data.exercises.findIndex((item) => item.id === currentExercise.id) + 1)} из {data.exercises.length}</span><span>~ 3 минуты</span></div>
                    <p className="exercise-prompt">{currentExercise.prompt}</p>
                    <label htmlFor="answer">Ваш ответ</label>
                    <textarea id="answer" value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder={currentExercise.skill_id === "skill_fastapi_routes" ? '{"status": "ok"}' : "Напишите код здесь…"} rows={5} spellCheck={false} />
                    <div className="exercise-actions"><span>Ответ проверит учебный движок</span><button className="primary-button" disabled={!answer.trim() || submitting} type="submit">{submitting ? <LoaderCircle className="spin" size={18} /> : <Send size={18} />}{submitting ? "Проверяем…" : "Проверить ответ"}</button></div>
                  </form>
                ) : <p>Упражнения пока не добавлены.</p>}

                {result && (
                  <div className={`result-panel ${result.is_correct ? "result-panel--success" : "result-panel--error"}`}>
                    <div className="result-panel__icon">{result.is_correct ? <Check size={22} /> : <RotateCcw size={21} />}</div>
                    <div><strong>{result.is_correct ? "Верно! Прогресс обновлён" : "Почти получилось"}</strong><p>{result.is_correct ? `Уровень навыка вырос с ${result.old_mastery} до ${result.new_mastery}.` : "Проверьте ответ и попробуйте ещё раз — прогресс не потерян."}</p></div>
                    {result.is_correct && result.recommendation.exercise_id && <button type="button" onClick={moveToRecommendation}>Дальше <ArrowRight size={17} /></button>}
                  </div>
                )}
              </section>

              <aside className="right-column">
                <section className="recommendation-card">
                  <div className="recommendation-card__icon"><Sparkles size={20} /></div>
                  <span className="section-kicker">Умная рекомендация</span>
                  <h3>{getRecommendationTitle(data.recommendation?.type)}</h3>
                  <p>{data.recommendation?.reason ?? "Выполните первое упражнение, чтобы получить рекомендацию."}</p>
                  {data.recommendation?.exercise_id && <button className="text-button" onClick={moveToRecommendation}>Перейти к заданию <ChevronRight size={17} /></button>}
                </section>

                <section className="path-card" id="path">
                  <div className="section-heading section-heading--compact"><div><span className="section-kicker">Учебный путь</span><h3>Навыки курса</h3></div><span>{completedSkills}/{data.knowledge.length}</span></div>
                  <div className="skill-list">
                    {data.knowledge.map((skill, index) => (
                      <div className="skill-row" key={skill.skill_id}>
                        <div className={`skill-step ${skill.mastery >= 70 ? "skill-step--done" : index === 0 || skill.mastery > 0 ? "skill-step--active" : ""}`}>{skill.mastery >= 70 ? <Check size={15} /> : index + 1}</div>
                        <div className="skill-info"><div><strong>{getSkillName(skill.skill_id)}</strong><span>{getLevelLabel(skill.level)}</span></div><div className="progress-track"><span style={{ width: `${skill.mastery}%` }} /></div></div>
                        <b>{Math.round(skill.mastery)}%</b>
                      </div>
                    ))}
                  </div>
                  <button className="reset-button" onClick={() => void handleReset()} disabled={resetting}><RotateCcw className={resetting ? "spin" : ""} size={16} />{resetting ? "Сбрасываем…" : "Сбросить демо-прогресс"}</button>
                </section>
              </aside>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
