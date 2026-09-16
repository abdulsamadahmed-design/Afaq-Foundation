import { Routes, Route, Link } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetails from "./pages/ProjectDetails";
import Donate from "./pages/Donate";


function Simple({ title, text }) {
  return (
    <main className="simple">
      <span className="eyebrow">
        AFAQ FOUNDATION
      </span>

      <h1>{title}</h1>

      <p>{text}</p>

      <Link className="btn" to="/">
        Back home
      </Link>
    </main>
  );
}


function Public({ children }) {
  return (
    <>
      <Navbar />

      {children}

      <footer>
        <p>
          © 2026 Afaq Foundation. Building
          stronger communities together.
        </p>
      </footer>
    </>
  );
}


export default function App() {
  return (
    <Routes>

      {/* Home */}
      <Route
        path="/"
        element={
          <Public>
            <Home />
          </Public>
        }
      />


      {/* Authentication */}
      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />


      {/* Dashboard */}
      <Route
        path="/dashboard"
        element={<Dashboard />}
      />


      {/* Projects */}
      <Route
        path="/projects"
        element={
          <Public>
            <Projects />
          </Public>
        }
      />

      <Route
        path="/projects/:id"
        element={
          <Public>
            <ProjectDetails />
          </Public>
        }
      />


      {/* Donations */}
      <Route
        path="/donate"
        element={
          <Public>
            <Donate />
          </Public>
        }
      />


      {/* Temporary pages */}
      {[
        [
          "about",
          "About Afaq",
          "Our story, mission, values and governance will live here.",
        ],

        [
          "programs",
          "Our Programs",
          "Education, community care, youth empowerment and development programs.",
        ],

        [
          "events",
          "Events",
          "Discover community events, workshops and upcoming activities.",
        ],

        [
          "volunteer",
          "Volunteer",
          "Join Afaq and contribute your time, skills and energy.",
        ],
      ].map(([path, title, text]) => (
        <Route
          key={path}
          path={"/" + path}
          element={
            <Public>
              <Simple
                title={title}
                text={text}
              />
            </Public>
          }
        />
      ))}

    </Routes>
  );
}
