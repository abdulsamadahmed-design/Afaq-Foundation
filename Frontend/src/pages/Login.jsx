import { Link } from "react-router-dom";
import { HeartHandshake } from "lucide-react";
export default function Login() {
  return (
    <main className="auth">
      <section className="auth-side">
        <HeartHandshake size={42} />
        <h1>Welcome back to Afaq.</h1>
        <p>
          Manage your profile, projects, donations and community activity from
          one place.
        </p>
      </section>
      <form className="auth-form">
        <span className="eyebrow">MEMBER ACCESS</span>
        <h2>Sign in</h2>
        <p>Enter your details to continue.</p>
        <label>
          Email address
          <input type="email" placeholder="you@example.com" />
        </label>
        <label>
          Password
          <input type="password" placeholder="••••••••" />
        </label>
        <div className="form-row">
          <label className="check">
            <input type="checkbox" /> Remember me
          </label>
          <a href="#">Forgot password?</a>
        </div>
        <button className="btn full" type="button">
          Sign in
        </button>
        <p className="form-foot">
          New to Afaq? <Link to="/register">Create an account</Link>
        </p>
      </form>
    </main>
  );
}
