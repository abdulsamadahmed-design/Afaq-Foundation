import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  Search,
  ArrowRight,
  MapPin,
  Users,
} from "lucide-react";

import { getProjects } from "../services/projectsApi";
import { categories } from "../data/projects";


const money = (n = 0) =>
  "KSh " + Number(n).toLocaleString();


export default function Projects() {
  const [projects, setProjects] = useState([]);

  const [filter, setFilter] = useState("All");
  const [status, setStatus] = useState("All");
  const [q, setQ] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    async function loadProjects() {
      try {
        setLoading(true);

        const data = await getProjects();

        const formattedProjects = data.map((project) => ({
          id: project.id,
          title: project.title,

          category: project.category,

          status:
            project.status.charAt(0).toUpperCase() +
            project.status.slice(1),

          summary: project.summary || project.description,
          description: project.description,

          target: project.target_amount,

          raised: project.amount_raised,

          location: project.location,

          beneficiaries: project.beneficiaries,
          icon: project.icon,
        }));

        setProjects(formattedProjects);
        setError("");
      } catch (err) {
        console.error(err);

        setError(
          "Unable to load projects. Please try again."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);


  const visible = useMemo(
    () =>
      projects.filter(
        (p) =>
          (filter === "All" ||
            p.category === filter) &&
          (status === "All" ||
            p.status === status) &&
          `${p.title} ${p.summary}`
            .toLowerCase()
            .includes(q.toLowerCase())
      ),
    [projects, filter, status, q]
  );


  const activeProjects = projects.filter(
    (p) => p.status === "Active"
  ).length;

  const totalBeneficiaries = projects.reduce(
    (total, project) =>
      total + project.beneficiaries,
    0
  );

  const totalRaised = projects.reduce(
    (total, project) =>
      total + project.raised,
    0
  );


  if (loading) {
    return (
      <main className="projects-page">
        <section className="project-browser">
          <div className="empty-projects">
            <b>Loading projects...</b>
            <p>
              Connecting to Afaq Foundation.
            </p>
          </div>
        </section>
      </main>
    );
  }


  if (error) {
    return (
      <main className="projects-page">
        <section className="project-browser">
          <div className="empty-projects">
            <b>Could not load projects.</b>
            <p>{error}</p>
          </div>
        </section>
      </main>
    );
  }


  return (
    <main className="projects-page">

      <section className="projects-hero">
        <span className="eyebrow">
          OUR WORK
        </span>

        <h1>
          Projects built around{" "}
          <em>real needs.</em>
        </h1>

        <p>
          Explore the initiatives Afaq is
          supporting, follow their progress
          and see exactly where help is needed.
        </p>

        <div className="project-summary">

          <div>
            <b>{activeProjects}</b>
            <span>Active projects</span>
          </div>

          <div>
            <b>
              {totalBeneficiaries.toLocaleString()}+
            </b>

            <span>
              Planned & reached beneficiaries
            </span>
          </div>

          <div>
            <b>{money(totalRaised)}</b>

            <span>
              Raised across projects
            </span>
          </div>

        </div>
      </section>


      <section className="project-browser">

        <div className="browser-top">

          <div className="searchbox">
            <Search size={19} />

            <input
              value={q}
              onChange={(e) =>
                setQ(e.target.value)
              }
              placeholder="Search projects..."
            />
          </div>

          <select
            value={status}
            onChange={(e) =>
              setStatus(e.target.value)
            }
          >
            <option>All</option>
            <option>Active</option>
            <option>Upcoming</option>
            <option>Completed</option>
          </select>

        </div>


        <div className="chips">

          {categories.map((c) => (
            <button
              className={
                filter === c ? "active" : ""
              }
              onClick={() => setFilter(c)}
              key={c}
            >
              {c}
            </button>
          ))}

        </div>


        <div className="results-head">

          <h2>
            {filter === "All"
              ? "All projects"
              : filter}
          </h2>

          <span>
            {visible.length} project
            {visible.length !== 1 ? "s" : ""}
          </span>

        </div>


        {visible.length ? (

          <div className="projects-list">

            {visible.map((p) => {

              const pct = Math.min(
                100,
                Math.round(
                  (p.raised / p.target) * 100
                ) || 0
              );

              return (
                <article
                  className="project-card-wide"
                  key={p.id}
                >

                  <div className="project-cover">

                    <span className="project-emoji">
                      {p.icon}
                    </span>

                    <span
                      className={
                        "status " +
                        p.status.toLowerCase()
                      }
                    >
                      {p.status}
                    </span>

                    <small>
                      {p.category}
                    </small>

                  </div>


                  <div className="project-info">

                    <div>
                      <h3>{p.title}</h3>
                      <p>{p.summary}</p>
                    </div>


                    <div className="project-meta">

                      <span>
                        <MapPin size={16} />
                        {p.location}
                      </span>

                      <span>
                        <Users size={16} />
                        {p.beneficiaries}{" "}
                        beneficiaries
                      </span>

                    </div>


                    <div>

                      <div className="funding-line">

                        <strong>
                          {money(p.raised)} raised
                        </strong>

                        <span>
                          {pct}% of{" "}
                          {money(p.target)}
                        </span>

                      </div>

                      <div className="progress">
                        <i
                          style={{
                            width: pct + "%",
                          }}
                        />
                      </div>

                    </div>


                    <div className="project-actions">

                      <Link
                        className="ghost"
                        to={"/projects/" + p.id}
                      >
                        View project{" "}
                        <ArrowRight size={16} />
                      </Link>

                      {p.status === "Active" && (
                        <Link
                          className="btn compact"
                          to={
                            "/donate?project=" +
                            p.id
                          }
                        >
                          Support project
                        </Link>
                      )}

                    </div>

                  </div>

                </article>
              );
            })}

          </div>

        ) : (

          <div className="empty-projects">
            <b>No projects found.</b>

            <p>
              Try another category or
              search term.
            </p>
          </div>

        )}

      </section>

    </main>
  );
}