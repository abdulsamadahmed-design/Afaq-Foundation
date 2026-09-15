import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  MapPin,
  Users,
  CalendarDays,
} from "lucide-react";
import { projects } from "../data/projects";
const money = (n) => "KSh " + n.toLocaleString();
export default function ProjectDetails() {
  const { id } = useParams();
  const p = projects.find((x) => x.id === id);
  if (!p)
    return (
      <main className="simple">
        <h1>Project not found</h1>
        <Link className="btn" to="/projects">
          Back to projects
        </Link>
      </main>
    );
  const pct = Math.min(100, Math.round((p.raised / p.target) * 100) || 0);
  return (
    <main className="detail-page">
      <section className="detail-top">
        <Link className="back" to="/projects">
          <ArrowLeft size={17} /> All projects
        </Link>
        <div className="detail-grid">
          <div>
            <div className="detail-tags">
              <span>{p.category}</span>
              <span className={"status " + p.status.toLowerCase()}>
                {p.status}
              </span>
            </div>
            <h1>{p.title}</h1>
            <p className="lead">{p.summary}</p>
            <div className="detail-meta">
              <span>
                <MapPin /> {p.location}
              </span>
              <span>
                <Users /> {p.beneficiaries} beneficiaries
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
          <span className="eyebrow">ABOUT THE PROJECT</span>
          <h2>Creating practical, measurable impact.</h2>
          <p>{p.description}</p>
          <h3>Project goals</h3>
          <div className="goal-list">
            {p.goals.map((g) => (
              <div key={g}>
                <CheckCircle2 />
                <span>{g}</span>
              </div>
            ))}
          </div>
          <h3>Latest updates</h3>
          <div className="timeline">
            {p.updates.map(([d, t]) => (
              <article key={d}>
                <CalendarDays />
                <div>
                  <b>{d}</b>
                  <p>{t}</p>
                </div>
              </article>
            ))}
          </div>
        </div>
        <aside className="fund-card">
          <span>FUNDING PROGRESS</span>
          <h2>{money(p.raised)}</h2>
          <p>raised of {money(p.target)} goal</p>
          <div className="progress large">
            <i style={{ width: pct + "%" }} />
          </div>
          <div className="fund-stats">
            <b>{pct}% funded</b>
            <span>{p.beneficiaries} beneficiaries</span>
          </div>
          {p.status === "Active" ? (
            <Link className="btn full" to={"/donate?project=" + p.id}>
              Donate to this project
            </Link>
          ) : (
            <Link className="ghost full" to="/projects">
              Explore active projects
            </Link>
          )}
          <small>
            Afaq's donation backend and payment processing will be connected in
            a later stage.
          </small>
        </aside>
      </section>
    </main>
  );
}
