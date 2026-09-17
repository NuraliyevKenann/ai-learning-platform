import { useEffect, useMemo, useState } from "react";
import {
  ArrowRight, BookOpen, Bot, Check, ChevronRight, CircleHelp, Flame,
  Languages, LoaderCircle, LogOut, RefreshCw, RotateCcw,
  Moon, Search, Send, ShieldCheck, Sparkles, Sun, Target, XCircle,
} from "lucide-react";

import { getMe, logout } from "../api/auth";
import { submitAttempt } from "../api/attempts";
import { API_DOCS_URL, AUTH_REQUIRED_EVENT } from "../api/client";
import { getExercises } from "../api/exercises";
import { getGoals } from "../api/goals";
import { getKnowledgeState, resetKnowledgeState } from "../api/knowledge";
import { getCurrentRecommendation } from "../api/recommendations";
import { getTopics } from "../api/topics";
import { AuthScreen } from "../components/AuthScreen";
import type { AttemptResult, Exercise, Goal, KnowledgeStateItem, Recommendation, Topic, User } from "../types/domain";

type Language = "ru" | "en";
type CourseId = "python" | "ml" | "cybersecurity";
type ActivePage = "recommendations" | "my-learning" | "progress" | "search";
type ThemeMode = "light" | "dark";

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

function getLevelLabel(level: string, isEnglish: boolean) {
  const labels = isEnglish
    ? { weak: "Needs work", practicing: "Practicing", strong: "Mastered" }
    : { weak: "Нужно изучить", practicing: "В процессе", strong: "Освоено" };
  return (labels as Record<string, string>)[level] ?? level;
}

function getRecommendationTitle(type: Recommendation["type"] | undefined, isEnglish: boolean) {
  if (type === "retry_exercise") return isEnglish ? "Try again" : "Попробуйте ещё раз";
  if (type === "next_exercise") return isEnglish ? "Next step is ready" : "Следующий шаг готов";
  if (type === "complete_goal") return isEnglish ? "Goal completed" : "Цель достигнута";
  return isEnglish ? "Start with the basics" : "Начните с основ";
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
  const [toast, setToast] = useState<string | null>(null);
  const [progressPulseKey, setProgressPulseKey] = useState(0);
  const [language, setLanguage] = useState<Language>("ru");
  const [selectedCourseId, setSelectedCourseId] = useState<CourseId>("python");
  const [activePage, setActivePage] = useState<ActivePage>("recommendations");
  const [themeMode, setThemeMode] = useState<ThemeMode>("light");
  const [courseSearch, setCourseSearch] = useState("");

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
    let isMounted = true;
    const fallbackTimeout = window.setTimeout(() => {
      if (!isMounted) return;
      setUser(null);
      setAuthLoading(false);
    }, 3000);

    void getMe()
      .then((currentUser) => {
        if (isMounted) setUser(currentUser);
      })
      .catch(() => {
        if (isMounted) setUser(null);
      })
      .finally(() => {
        if (!isMounted) return;
        window.clearTimeout(fallbackTimeout);
        setAuthLoading(false);
      });

    return () => {
      isMounted = false;
      window.clearTimeout(fallbackTimeout);
    };
  }, []);

  useEffect(() => {
    const handleUnauthorized = () => setUser(null);
    window.addEventListener(AUTH_REQUIRED_EVENT, handleUnauthorized);
    return () => window.removeEventListener(AUTH_REQUIRED_EVENT, handleUnauthorized);
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
  const isEnglish = language === "en";
  const isDarkMode = themeMode === "dark";
  const copy = {
    navRecommendations: isEnglish ? "Recommendations" : "Рекомендации",
    navMyLearning: isEnglish ? "My learning" : "Моё обучение",
    navProgress: isEnglish ? "Progress" : "Прогресс",
    navSearch: isEnglish ? "Search" : "Поиск",
    learningLabel: isEnglish ? "Your learning" : "Ваше обучение",
    welcome: isEnglish ? "Welcome back!" : "С возвращением!",
    streak: isEnglish ? "3 day streak" : "3 дня подряд",
    refresh: isEnglish ? "Refresh data" : "Обновить данные",
    chooseTrack: isEnglish ? "Choose a learning track" : "Выберите направление обучения",
    courseCount: isEnglish ? "tracks" : "направления",
    searchCourses: isEnglish ? "Search courses" : "Поиск курсов",
    searchCoursesTitle: isEnglish ? "Type what you want to learn" : "Напишите, что хотите изучать",
    searchCoursesPlaceholder: isEnglish ? "Python, ML, security..." : "Python, ML, безопасность...",
    noCoursesFound: isEnglish ? "No courses found yet. Try another keyword." : "Пока ничего не найдено. Попробуйте другое слово.",
    openMyLearning: isEnglish ? "Open my learning" : "Открыть моё обучение",
    chooseCourse: isEnglish ? "Choose course" : "Выбрать курс",
    currentCourse: isEnglish ? "Current course" : "Текущий курс",
    planned: isEnglish ? "Planned" : "В плане",
    learned: isEnglish ? "learned" : "освоено",
    skillsComplete: isEnglish ? "skills completed" : "навыков завершено",
    overallProgress: isEnglish ? "Overall progress" : "Общий прогресс",
    bySkills: isEnglish ? "by skills" : "по навыкам",
    completedSkills: isEnglish ? "Completed skills" : "Освоено навыков",
    recommendedNow: isEnglish ? "Recommended now" : "Рекомендовано сейчас",
    currentExercise: isEnglish ? "Current exercise" : "Текущее упражнение",
    beginner: isEnglish ? "Beginner" : "Начальный",
    exercise: isEnglish ? "Exercise" : "Задание",
    of: isEnglish ? "of" : "из",
    minutes: isEnglish ? "~ 3 minutes" : "~ 3 минуты",
    yourAnswer: isEnglish ? "Your answer" : "Ваш ответ",
    writeCode: isEnglish ? "Write code here..." : "Напишите код здесь…",
    engineChecks: isEnglish ? "The learning engine will check your answer" : "Ответ проверит учебный движок",
    checking: isEnglish ? "Checking..." : "Проверяем…",
    checkAnswer: isEnglish ? "Check answer" : "Проверить ответ",
    noExercises: isEnglish ? "Exercises are not added yet." : "Упражнения пока не добавлены.",
    correct: isEnglish ? "Correct! Progress updated" : "Верно! Прогресс обновлён",
    almost: isEnglish ? "Almost there" : "Почти получилось",
    tryAgain: isEnglish ? "Check the answer and try again — your progress is saved." : "Проверьте ответ и попробуйте ещё раз — прогресс не потерян.",
    next: isEnglish ? "Next" : "Дальше",
    smartRecommendation: isEnglish ? "Smart recommendation" : "Умная рекомендация",
    firstExercise: isEnglish ? "Complete the first exercise to get a recommendation." : "Выполните первое упражнение, чтобы получить рекомендацию.",
    goToExercise: isEnglish ? "Go to exercise" : "Перейти к заданию",
    learningPath: isEnglish ? "Learning path" : "Учебный путь",
    courseSkills: isEnglish ? "Course skills" : "Навыки курса",
    resetting: isEnglish ? "Resetting..." : "Сбрасываем…",
    resetDemo: isEnglish ? "Reset demo progress" : "Сбросить демо-прогресс",
    searchTitle: isEnglish ? "Find a topic or exercise" : "Найдите тему или задание",
    searchPlaceholder: isEnglish ? "For example: FastAPI, SQL, variables" : "Например: FastAPI, SQL, переменные",
    aiAssistant: isEnglish ? "AI assistant" : "ИИ ассистент",
    darkMode: isEnglish ? "Dark mode" : "Тёмная тема",
    lightMode: isEnglish ? "Light mode" : "Светлая тема",
  };
  const courseOptions = [
    {
      id: "python" as const,
      title: "Python Backend",
      status: copy.currentCourse,
      description: isEnglish ? "FastAPI, API, databases, and backend foundation." : "FastAPI, API, базы данных и основа backend.",
      learningTitle: data.goals[0]?.title ?? "Python Backend Developer",
      learningDescription: data.goals[0]?.description ?? (isEnglish ? "Learn through short practical exercises." : "Учитесь через короткие практические задания."),
      keywords: "python backend fastapi api sql база базы данных сервер",
    },
    {
      id: "ml" as const,
      title: "ML Engineer",
      status: copy.planned,
      description: isEnglish ? "Data, models, evaluation, and production ML workflow." : "Данные, модели, evaluation и production ML workflow.",
      learningTitle: "ML Engineer",
      learningDescription: isEnglish ? "This path will include data preparation, model evaluation, and ML systems." : "Это направление будет включать подготовку данных, evaluation и ML systems.",
      keywords: "machine learning ml engineer data models модели данные ии ai",
    },
    {
      id: "cybersecurity" as const,
      title: "Cybersecurity",
      status: copy.planned,
      description: isEnglish ? "Web security, auth, threats, and secure backend basics." : "Web security, auth, threats и основы безопасного backend.",
      learningTitle: "Cybersecurity",
      learningDescription: isEnglish ? "This path will focus on web security, auth flows, and secure backend habits." : "Это направление будет про web security, auth flows и привычки безопасного backend.",
      keywords: "cybersecurity security cyber безопасность кибербезопасность auth threats",
    },
  ];
  const selectedCourse = courseOptions.find((course) => course.id === selectedCourseId) ?? courseOptions[0];
  const normalizedCourseSearch = courseSearch.trim().toLowerCase();
  const filteredCourseOptions = normalizedCourseSearch
    ? courseOptions.filter((course) =>
      `${course.title} ${course.description} ${course.learningDescription} ${course.keywords}`.toLowerCase().includes(normalizedCourseSearch),
    )
    : courseOptions;

  useEffect(() => {
    if (!toast) return;
    const timeoutId = window.setTimeout(() => setToast(null), 2600);
    return () => window.clearTimeout(timeoutId);
  }, [toast]);

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
      setToast(attempt.is_correct ? "Ответ принят. Прогресс обновлён." : "Ответ сохранён. Попробуйте ещё раз.");
      setProgressPulseKey((key) => key + 1);
      if (attempt.is_correct) {
        setAnswer("");
      }
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
      setToast("Прогресс сброшен.");
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

  function selectCourse(courseId: CourseId) {
    setSelectedCourseId(courseId);
    setActivePage("my-learning");
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
    <div className={`app-shell theme-${themeMode}`}>
      {toast && (
        <div className="toast-notice" role="status">
          <Check size={17} />
          <span>{toast}</span>
        </div>
      )}
      <header className="app-header">
        <button className="app-brand app-brand--button" type="button" onClick={() => setActivePage("recommendations")} aria-label="SkillWay home">
          <span className="brand__mark"><Sparkles size={20} strokeWidth={2.2} /></span>
          <strong>SkillWay</strong>
        </button>
        <nav className="top-nav" aria-label={isEnglish ? "Main navigation" : "Главная навигация"}>
          <button className={`top-nav__link ${activePage === "recommendations" ? "top-nav__link--active" : ""}`} type="button" onClick={() => setActivePage("recommendations")}><Sparkles size={18} /> {copy.navRecommendations}</button>
          <button className={`top-nav__link ${activePage === "my-learning" ? "top-nav__link--active" : ""}`} type="button" onClick={() => setActivePage("my-learning")}><BookOpen size={18} /> {copy.navMyLearning}</button>
          <button className={`top-nav__link ${activePage === "progress" ? "top-nav__link--active" : ""}`} type="button" onClick={() => setActivePage("progress")}><Target size={18} /> {copy.navProgress}</button>
          <button className={`top-nav__link ${activePage === "search" ? "top-nav__link--active" : ""}`} type="button" onClick={() => setActivePage("search")}><Search size={18} /> {copy.navSearch}</button>
          <a className="top-nav__link top-nav__link--muted" href={API_DOCS_URL} target="_blank" rel="noreferrer"><CircleHelp size={18} /> API</a>
        </nav>
        <div className="top-actions">
          <button className="top-action-button" type="button" onClick={() => setLanguage(isEnglish ? "ru" : "en")} title={isEnglish ? "Switch to Russian" : "Сменить язык на английский"}><Languages size={17} /> {language.toUpperCase()}</button>
          <button className="top-action-button" type="button" onClick={() => setThemeMode(isDarkMode ? "light" : "dark")} title={isDarkMode ? copy.lightMode : copy.darkMode}>{isDarkMode ? <Sun size={17} /> : <Moon size={17} />} {isDarkMode ? (isEnglish ? "Light" : "Светлая") : (isEnglish ? "Dark" : "Тёмная")}</button>
          <button className="top-action-button top-action-button--ai" type="button" title={copy.aiAssistant}><Bot size={17} /> AI</button>
        </div>
        <div className="top-profile">
          <div className="avatar">{getInitials(user.display_name)}</div>
          <div><strong>{user.display_name}</strong><span>{user.email}</span></div>
          <button className="profile-logout" onClick={() => void handleLogout()} aria-label="Выйти из аккаунта" title="Выйти"><LogOut size={18} /></button>
        </div>
      </header>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div><p className="eyebrow">{copy.learningLabel}</p><h1>{copy.welcome}</h1></div>
          <div className="topbar__actions">
            <div className="streak"><Flame size={17} fill="currentColor" /> {copy.streak}</div>
            <button className="icon-button" onClick={() => void loadDashboard()} aria-label={copy.refresh} title={copy.refresh}><RefreshCw size={19} /></button>
          </div>
        </header>

        {error && <div className="error-banner" role="alert"><XCircle size={19} /><span>{error}. {isEnglish ? "Check that the backend is running on port 8000." : "Проверьте, что backend запущен на порту 8000."}</span><button onClick={() => void loadDashboard()}>{isEnglish ? "Retry" : "Повторить"}</button></div>}

        {loading ? (
          <div className="loading-state"><LoaderCircle className="spin" size={28} /> {isEnglish ? "Loading your learning plan..." : "Загружаем ваш учебный план…"}</div>
        ) : (
          <>
            {activePage === "search" && (
              <section className="search-card search-card--courses" id="search" aria-label={copy.searchCourses}>
                <div><span className="section-kicker">{copy.searchCourses}</span><h3>{copy.searchCoursesTitle}</h3></div>
                <label className="search-box">
                  <Search size={18} />
                  <input value={courseSearch} onChange={(event) => setCourseSearch(event.target.value)} type="search" placeholder={copy.searchCoursesPlaceholder} aria-label={copy.searchCourses} />
                </label>
              </section>
            )}

            {(activePage === "recommendations" || activePage === "search") && (
              <section className="course-recommendations" id="course-recommendations" aria-label={isEnglish ? "Recommended tracks" : "??????????????? ???????????"}>
                <div className="section-heading course-recommendations__heading">
                  <div><span className="section-kicker">{copy.navRecommendations}</span><h2>{copy.chooseTrack}</h2></div>
                  <span>{filteredCourseOptions.length} {copy.courseCount}</span>
                </div>
                {filteredCourseOptions.length ? (
                  <div className="course-grid">
                    {filteredCourseOptions.map((course) => (
                      <article className={`course-card ${selectedCourseId === course.id ? "course-card--active" : ""}`} key={course.id}>
                        <div className="course-card__icon">
                          {course.id === "python" ? <BookOpen size={22} /> : course.id === "ml" ? <Sparkles size={22} /> : <ShieldCheck size={22} />}
                        </div>
                        <span>{course.status}</span>
                        <h3>{course.title}</h3>
                        <p>{course.description}</p>
                        <button type="button" onClick={() => selectCourse(course.id)}>
                          {selectedCourseId === course.id ? copy.openMyLearning : copy.chooseCourse}
                          <ChevronRight size={16} />
                        </button>
                      </article>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">{copy.noCoursesFound}</div>
                )}
              </section>
            )}

            {(activePage === "my-learning" || activePage === "progress") && (
              <>
                <section className="welcome-card" id="my-learning">
                  <div>
                    <span className="status-pill"><span /> {copy.navMyLearning}</span>
                    <h2>{selectedCourse.learningTitle}</h2>
                    <p>{selectedCourse.learningDescription}</p>
                  </div>
                  <div className="goal-progress">
                    <div className="goal-progress__ring" style={{ "--progress": `${averageMastery * 3.6}deg` } as React.CSSProperties}><div><strong>{averageMastery}%</strong><span>{copy.learned}</span></div></div>
                    <p>{completedSkills} {copy.of} {data.knowledge.length} {copy.skillsComplete}</p>
                  </div>
                </section>

                <section className="stats-grid" id="progress" aria-label={isEnglish ? "Learning stats" : "Статистика обучения"}>
                  <article className="stat-card stat-card--pulse" key={progressPulseKey}><div className="stat-icon stat-icon--blue"><Target size={20} /></div><div><span>{copy.overallProgress}</span><strong>{averageMastery}%</strong></div><span className="stat-trend">{copy.bySkills}</span></article>
                  <article className="stat-card"><div className="stat-icon stat-icon--mint"><Check size={20} /></div><div><span>{copy.completedSkills}</span><strong>{completedSkills}</strong></div><span className="stat-trend">{copy.of} {data.knowledge.length}</span></article>
                </section>

                <div className="dashboard-grid">
                  <section className="exercise-card" id="exercise">
                    <div className="section-heading"><div><span className="section-kicker">{copy.recommendedNow}</span><h2>{currentTopic?.title ?? copy.currentExercise}</h2></div><span className="difficulty">{copy.beginner}</span></div>
                    {currentExercise ? (
                      <form onSubmit={handleSubmit}>
                        <div className="exercise-meta"><span>{copy.exercise} {Math.max(1, data.exercises.findIndex((item) => item.id === currentExercise.id) + 1)} {copy.of} {data.exercises.length}</span><span>{copy.minutes}</span></div>
                        <p className="exercise-prompt">{currentExercise.prompt}</p>
                        <label htmlFor="answer">{copy.yourAnswer}</label>
                        <textarea id="answer" value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder={currentExercise.skill_id === "skill_fastapi_routes" ? '{"status": "ok"}' : copy.writeCode} rows={5} spellCheck={false} />
                        <div className="exercise-actions"><span>{copy.engineChecks}</span><button className="primary-button" disabled={!answer.trim() || submitting} type="submit">{submitting ? <LoaderCircle className="spin" size={18} /> : <Send size={18} />}{submitting ? copy.checking : copy.checkAnswer}</button></div>
                      </form>
                    ) : <p>{copy.noExercises}</p>}

                    {result && (
                      <div className={`result-panel ${result.is_correct ? "result-panel--success" : "result-panel--error"}`}>
                        <div className="result-panel__icon">{result.is_correct ? <Check size={22} /> : <RotateCcw size={21} />}</div>
                        <div><strong>{result.is_correct ? copy.correct : copy.almost}</strong><p>{result.is_correct ? (isEnglish ? `Skill mastery grew from ${result.old_mastery} to ${result.new_mastery}.` : `Уровень навыка вырос с ${result.old_mastery} до ${result.new_mastery}.`) : copy.tryAgain}</p></div>
                        {result.is_correct && result.recommendation.exercise_id && <button type="button" onClick={moveToRecommendation}>{copy.next} <ArrowRight size={17} /></button>}
                      </div>
                    )}
                  </section>

                  <aside className="right-column">
                    <section className="recommendation-card" id="recommendations">
                      <div className="recommendation-card__icon"><Sparkles size={20} /></div>
                      <span className="section-kicker">{copy.smartRecommendation}</span>
                      <h3>{getRecommendationTitle(data.recommendation?.type, isEnglish)}</h3>
                      <p>{data.recommendation?.reason ?? copy.firstExercise}</p>
                      {data.recommendation?.exercise_id && <button className="text-button" onClick={moveToRecommendation}>{copy.goToExercise} <ChevronRight size={17} /></button>}
                    </section>

                    <section className="path-card" id="path">
                      <div className="section-heading section-heading--compact"><div><span className="section-kicker">{copy.learningPath}</span><h3>{copy.courseSkills}</h3></div><span>{completedSkills}/{data.knowledge.length}</span></div>
                      <div className="skill-list">
                        {data.knowledge.map((skill, index) => (
                          <div className="skill-row" key={skill.skill_id}>
                            <div className={`skill-step ${skill.mastery >= 70 ? "skill-step--done" : index === 0 || skill.mastery > 0 ? "skill-step--active" : ""}`}>{skill.mastery >= 70 ? <Check size={15} /> : index + 1}</div>
                            <div className="skill-info"><div><strong>{getSkillName(skill.skill_id)}</strong><span>{getLevelLabel(skill.level, isEnglish)}</span></div><div className="progress-track"><span style={{ width: `${skill.mastery}%` }} /></div></div>
                            <b>{Math.round(skill.mastery)}%</b>
                          </div>
                        ))}
                      </div>
                      <button className="reset-button" onClick={() => void handleReset()} disabled={resetting}><RotateCcw className={resetting ? "spin" : ""} size={16} />{resetting ? copy.resetting : copy.resetDemo}</button>
                    </section>
                  </aside>
                </div>
              </>
            )}
          </>
        )}
      </main>
    </div>
  );
}
