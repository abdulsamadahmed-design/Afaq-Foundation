import { Routes, Route, Link } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Login from "./pages/Login";
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
        <div>
          <b>AFAQ FOUNDATION</b>

          <p>
            Building brighter horizons through
            community-led action.
          </p>
        </div>

        <div>
          © 2026 Afaq Foundation • Built for impact.
        </div>
      </footer>
    </>
  );
}


export default function App() {
  return (
    <Routes>

      {/* HOME */}
      <Route
        path="/"
        element={
          <Public>
            <Home />
          </Public>
        }
      />


      {/* AUTH */}
      <Route
        path="/login"
        element={<Login />}
      />


      {/* DASHBOARD */}
      <Route
        path="/dashboard"
        element={<Dashboard />}
      />


      {/* PROJECTS */}
      <Route
        path="/projects"
        element={
          <Public>
            <Projects />
          </Public>
        }
      />


      {/* PROJECT DETAILS */}
      <Route
        path="/projects/:id"
        element={
          <Public>
            <ProjectDetails />
          </Public>
        }
      />


      {/* DONATE */}
      <Route
        path="/donate"
        element={
          <Public>
            <Donate />
          </Public>
        }
      />


      {/* PLACEHOLDER PAGES */}
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

        [
          "register",
          "Create Account",
          "Member registration will be connected to Afaq authentication later.",
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
