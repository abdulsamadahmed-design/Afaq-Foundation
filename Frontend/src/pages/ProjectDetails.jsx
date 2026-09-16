import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  MapPin,
  Users,
  CalendarDays,
} from "lucide-react";

import { getProject } from "../services/projectsApi";


const money = (n = 0) =>
  "KSh " + Number(n).toLocaleString();


export default function ProjectDetails() {
  const { id } = useParams();

  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    async function loadProject() {
      try {
        setLoading(true);

        const data = await getProject(id);

        const formattedProject = {
          id: data.id,
          title: data.title,
          category: data.category,

          status:
            data.status.charAt(0).toUpperCase() +
            data.status.slice(1),

          summary:
            data.summary || data.description,

          description: data.description,

          target: data.target_amount,
          raised: data.amount_raised,

          beneficiaries: data.beneficiaries,
          location: data.location,
          icon: data.icon,

          goals: data.goals || [],
          updates: data.updates || [],
        };

        setProject(formattedProject);
        setError("");
      } catch (err) {
        console.error(err);
        setError("Project not found.");
      } finally {
        setLoading(false);
      }
    }

    loadProject();
  }, [id]);


  if (loading) {
    return (
      <main className="simple">
        <h1>Loading project...</h1>
      </main>
    );
  }


  if (error || !project) {
    return (
      <main className="simple">
        <h1>Project not found</h1>

        <Link className="btn" to="/projects">
          Back to projects
        </Link>
      </main>
    );
  }


  const p = project;

  const pct = Math.min(
    100,
    Math.round(
      (p.raised / p.target) * 100
    ) || 0
  );


  return (
    <main className="detail-page">

      <section className="detail-top">

        <Link className="back" to="/projects">
          <ArrowLeft size={17} />
          All projects
        </Link>


        <div className="detail-grid">

          <div>

            <div className="detail-tags">

              <span>{p.category}</span>

              <span
                className={
                  "status " +
                  p.status.toLowerCase()
                }
              >
                {p.status}
              </span>

            </div>


            <h1>{p.title}</h1>

            <p className="lead">
              {p.summary}
            </p>


            <div className="detail-meta">

              <span>
                <MapPin />
                {p.location}
              </span>

              <span>
                <Users />
                {p.beneficiaries} beneficiaries
              </span>

            </div>

          </div>


          <div className="detail-art">
            <span>{p.icon}</span>
          </div>

        </div>

      </section>


      <section className="detail-content">

        <div className="detail-main">

          <span className="eyebrow">
            ABOUT THE PROJECT
          </span>

          <h2>
            Creating practical, measurable impact.
          </h2>

          <p>{p.description}</p>


          <h3>Project goals</h3>

          <div className="goal-list">

            {p.goals.map((goal, index) => (
              <div key={index}>

                <CheckCircle2 />

                <span>{goal}</span>

              </div>
            ))}

          </div>


          <h3>Latest updates</h3>

          <div className="timeline">

            {p.updates.map(
              ([title, text], index) => (

                <article key={index}>

                  <CalendarDays />

                  <div>

                    <b>{title}</b>

                    <p>{text}</p>

                  </div>

                </article>

              )
            )}

          </div>

        </div>


        <aside className="fund-card">

          <span>
            FUNDING PROGRESS
          </span>

          <h2>
            {money(p.raised)}
          </h2>

          <p>
            raised of {money(p.target)} goal
          </p>


          <div className="progress large">

            <i
              style={{
                width: pct + "%",
              }}
            />

          </div>


          <div className="fund-stats">

            <b>{pct}% funded</b>

            <span>
              {p.beneficiaries} beneficiaries
            </span>

          </div>


          {p.status === "Active" ? (

            <Link
              className="btn full"
              to={"/donate?project=" + p.id}
            >
              Donate to this project
            </Link>

          ) : (

            <Link
              className="ghost full"
              to="/projects"
            >
              Explore active projects
            </Link>

          )}


          <small>
            Afaq's donation backend and payment
            processing will be connected in a
            later stage.
          </small>

        </aside>

      </section>

    </main>
  );
}