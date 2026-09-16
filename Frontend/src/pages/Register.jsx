import { useState } from "react";
import {
  Link,
  useNavigate,
} from "react-router-dom";

import {
  HeartHandshake,
  UserPlus,
} from "lucide-react";

import {
  registerUser,
} from "../services/authApi";


export default function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] =
    useState("");
  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);
  const [error, setError] =
    useState("");


  async function handleSubmit(event) {
    event.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await registerUser(
        name,
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
        err.message ||
          "Unable to create account."
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
          Become part of Afaq.
        </h1>

        <p>
          Create your account to support
          projects, track donations and take
          part in community activities.
        </p>

      </section>


      <form
        className="auth-form"
        onSubmit={handleSubmit}
      >

        <span className="eyebrow">
          JOIN AFAQ
        </span>

        <h2>Create account</h2>

        <p>
          Enter your details to get started.
        </p>


        <label>
          Full name

          <input
            type="text"
            placeholder="Your full name"
            value={name}
            onChange={(event) =>
              setName(event.target.value)
            }
            required
          />
        </label>


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
            placeholder="Minimum 6 characters"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            minLength={6}
            required
          />
        </label>


        <label>
          Confirm password

          <input
            type="password"
            placeholder="Enter password again"
            value={confirmPassword}
            onChange={(event) =>
              setConfirmPassword(
                event.target.value
              )
            }
            minLength={6}
            required
          />
        </label>


        {error && (
          <p className="form-error">
            {error}
          </p>
        )}


        <button
          className="btn full"
          type="submit"
          disabled={loading}
        >
          <UserPlus size={17} />

          {loading
            ? "Creating account..."
            : "Create account"}
        </button>


        <p className="form-foot">
          Already have an account?{" "}

          <Link to="/login">
            Sign in
          </Link>
        </p>

      </form>

    </main>
  );
}
