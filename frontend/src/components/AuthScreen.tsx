import { useState } from "react";
import { ArrowRight, BookOpenCheck, Check, Eye, EyeOff, LoaderCircle, Sparkles } from "lucide-react";

import { login, register } from "../api/auth";
import type { User } from "../types/domain";

type AuthScreenProps = {
  onAuthenticated: (user: User) => void;
};

export function AuthScreen({ onAuthenticated }: AuthScreenProps) {
  const [mode, setMode] = useState<"login" | "register">("register");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function switchMode(nextMode: "login" | "register") {
    setMode(nextMode);
    setError(null);
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const user = mode === "register"
        ? await register({ display_name: displayName.trim(), email: email.trim(), password })
        : await login({ email: email.trim(), password });
      onAuthenticated(user);
    } catch (caughtError) {
      const message = caughtError instanceof Error ? caughtError.message : "Не удалось продолжить";
      if (message === "Email is already registered.") setError("Этот email уже зарегистрирован.");
      else if (message === "Invalid email or password.") setError("Неверный email или пароль.");
      else setError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-story">
        <div className="auth-brand"><span><Sparkles size={20} /></span> SkillWay</div>
        <div className="auth-story__content">
          <span className="auth-kicker">Персональный учебный маршрут</span>
          <h1>Учитесь с пониманием своего прогресса.</h1>
          <p>SkillWay оценивает ваши ответы, обновляет уровень навыков и подсказывает следующий полезный шаг.</p>
          <div className="auth-benefits">
            <div><span><Check size={16} /></span><p><strong>Личный прогресс</strong>Продолжайте с того места, где остановились.</p></div>
            <div><span><Check size={16} /></span><p><strong>Практика вместо догадок</strong>Каждое задание влияет на вашу карту навыков.</p></div>
            <div><span><Check size={16} /></span><p><strong>Следующий шаг</strong>Получайте рекомендацию после каждого ответа.</p></div>
          </div>
        </div>
        <div className="auth-story__quote"><BookOpenCheck size={21} /><span>Небольшие упражнения.<br />Видимый результат.</span></div>
      </section>

      <section className="auth-form-side">
        <div className="auth-card">
          <div className="auth-card__heading">
            <span>{mode === "register" ? "Новый аккаунт" : "С возвращением"}</span>
            <h2>{mode === "register" ? "Создайте свой профиль" : "Войдите в SkillWay"}</h2>
            <p>{mode === "register" ? "Начните персональный путь в Python backend." : "Ваш прогресс ждёт вас внутри."}</p>
          </div>

          <div className="auth-tabs" role="tablist">
            <button className={mode === "register" ? "active" : ""} onClick={() => switchMode("register")} type="button">Регистрация</button>
            <button className={mode === "login" ? "active" : ""} onClick={() => switchMode("login")} type="button">Вход</button>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            {mode === "register" && (
              <label>Ваше имя<input value={displayName} onChange={(event) => setDisplayName(event.target.value)} placeholder="Например, Алекс" minLength={2} maxLength={50} autoComplete="name" required /></label>
            )}
            <label>Email<input value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@example.com" type="email" autoComplete="email" required /></label>
            <label>Пароль<div className="password-field"><input value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Минимум 8 символов" type={showPassword ? "text" : "password"} minLength={8} maxLength={128} autoComplete={mode === "register" ? "new-password" : "current-password"} required /><button type="button" onClick={() => setShowPassword((visible) => !visible)} aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}>{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button></div></label>

            {error && <div className="auth-error" role="alert">{error}</div>}
            <button className="auth-submit" disabled={submitting} type="submit">
              {submitting ? <LoaderCircle className="spin" size={18} /> : <ArrowRight size={18} />}
              {submitting ? "Подождите…" : mode === "register" ? "Создать аккаунт" : "Войти"}
            </button>
          </form>
          <p className="auth-switch">{mode === "register" ? "Уже есть аккаунт?" : "Ещё нет аккаунта?"}<button onClick={() => switchMode(mode === "register" ? "login" : "register")} type="button">{mode === "register" ? "Войти" : "Зарегистрироваться"}</button></p>
        </div>
      </section>
    </main>
  );
}
