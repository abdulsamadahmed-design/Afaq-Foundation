import { useState } from "react";
import {
  Link,
  useNavigate,
} from "react-router-dom";
import { HeartHandshake } from "lucide-react";

import { loginUser } from "../services/authApi";


export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");

      const data = await loginUser(
        email,
        password
      );

      localStorage.setItem(
        "afaqUser",
        JSON.stringify(data.user)
      );

      navigate("/dashboard");
    } catch (err) {
      console.error(err);

      setError(
        err.message || "Unable to sign in."
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="auth">

      <section className="auth-side">

        <HeartHandshake size={42} />

        <h1>
          Welcome back to Afaq.
        </h1>

        <p>
          Manage your profile, projects,
          donations and community activity
          from one place.
        </p>

      </section>


      <form
        className="auth-form"
        onSubmit={handleSubmit}
      >

        <span className="eyebrow">
          MEMBER ACCESS
        </span>

        <h2>Sign in</h2>

        <p>
          Enter your details to continue.
        </p>


        <label>
          Email address

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
          />
        </label>


        <label>
          Password

          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />
        </label>


        {error && (
          <p className="form-error">
            {error}
          </p>
        )}


        <div className="form-row">

          <label className="check">
            <input type="checkbox" />
            Remember me
          </label>

          <a href="#">
            Forgot password?
          </a>

        </div>


        <button
          className="btn full"
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Signing in..."
            : "Sign in"}
        </button>


        <p className="form-foot">
          New to Afaq?{" "}

          <Link to="/register">
            Create an account
          </Link>
        </p>

      </form>

    </main>
  );
}
