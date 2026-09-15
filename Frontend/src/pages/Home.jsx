import { Link } from "react-router-dom";
import {
  ArrowRight,
  BookOpen,
  Heart,
  Users,
  CalendarDays,
  ShieldCheck,
  Quote,
} from "lucide-react";
const projects = [
  [
    "Education Without Barriers",
    "Help equip learners with books, mentorship and digital access.",
    72,
    360000,
    500000,
  ],
  [
    "Ramadan Food Support",
    "Deliver essential food packages to families facing hardship.",
    84,
    420000,
    500000,
  ],
  [
    "Youth Skills Lab",
    "Practical digital and career skills for young people.",
    56,
    280000,
    500000,
  ],
];
export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">COMMUNITY • DIGNITY • OPPORTUNITY</span>
          <h1>
            Building brighter <em>horizons</em>, together.
          </h1>
          <p>
            Afaq Foundation connects people, resources and practical programs to
            create lasting opportunities for communities.
          </p>
          <div className="actions">
            <Link className="btn" to="/donate">
              Make an impact <ArrowRight size={18} />
            </Link>
            <Link className="ghost" to="/projects">
              Explore our work
            </Link>
          </div>
          <div className="trust">
            <ShieldCheck /> Transparent giving <span /> Community-led programs{" "}
            <span /> Measurable impact
          </div>
        </div>
        <div className="hero-art">
          <div className="sun"></div>
          <div className="impact-card">
            <b>2,480+</b>
            <small>people reached this year</small>
            <div className="avatars">
              ● ● ● ● <strong>+2K</strong>
            </div>
          </div>
          <div className="quote-card">
            “Hope grows when opportunity becomes accessible.”
          </div>
        </div>
      </section>
      <section className="stats">
        <div>
          <b>12+</b>
          <span>Active projects</span>
        </div>
        <div>
          <b>2.4K</b>
          <span>People reached</span>
        </div>
        <div>
          <b>680</b>
          <span>Volunteers</span>
        </div>
        <div>
          <b>92%</b>
          <span>Funds to programs</span>
        </div>
      </section>
      <section className="section intro">
        <span className="eyebrow">WHAT WE DO</span>
        <h2>Impact that goes beyond a donation.</h2>
        <p>
          We focus on practical programs that strengthen people and communities
          for the long term.
        </p>
        <div className="program-grid">
          {[
            [
              BookOpen,
              "Education",
              "Learning access, mentorship and school support.",
            ],
            [
              Heart,
              "Community Care",
              "Food, emergency relief and family support.",
            ],
            [
              Users,
              "Youth Empowerment",
              "Skills, leadership and pathways to opportunity.",
            ],
            [
              CalendarDays,
              "Community Events",
              "Programs that connect, teach and mobilize.",
            ],
          ].map(([I, t, d]) => (
            <article className="program" key={t}>
              <I />
              <h3>{t}</h3>
              <p>{d}</p>
              <Link to="/programs">Learn more →</Link>
            </article>
          ))}
        </div>
      </section>
      <section className="section projects">
        <div className="section-head">
          <div>
            <span className="eyebrow">FEATURED PROJECTS</span>
            <h2>See where your support goes.</h2>
          </div>
          <Link to="/projects">View all projects →</Link>
        </div>
        <div className="project-grid">
          {projects.map(([n, d, p, r, g]) => (
            <article className="project" key={n}>
              <div className="project-image">
                <span>ACTIVE</span>
              </div>
              <div className="project-body">
                <h3>{n}</h3>
                <p>{d}</p>
                <div className="progress">
                  <i style={{ width: p + "%" }} />
                </div>
                <div className="money">
                  <b>KSh {r.toLocaleString()}</b>
                  <span>of KSh {g.toLocaleString()}</span>
                </div>
                <Link className="project-link" to="/donate">
                  Support this project <ArrowRight size={16} />
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>
      <section className="section story">
        <div className="story-visual">
          <div className="story-badge">
            <b>680</b>
            <span>active volunteers</span>
          </div>
        </div>
        <div>
          <span className="eyebrow">VOLUNTEER WITH AFAQ</span>
          <h2>Your time can change someone's tomorrow.</h2>
          <p>
            Whether you can mentor, organize an event, share a professional
            skill or simply lend a hand, there is a place for you at Afaq.
          </p>
          <Link className="btn" to="/volunteer">
            Become a volunteer <ArrowRight size={18} />
          </Link>
        </div>
      </section>
      <section className="section testimonial">
        <Quote />
        <p>
          We believe transparency is part of the impact. Every project should
          have a clear purpose, visible progress and accountable use of
          resources.
        </p>
        <strong>Afaq Foundation</strong>
        <span>Impact & Transparency Commitment</span>
      </section>
      <section className="cta">
        <span className="eyebrow">START TODAY</span>
        <h2>A small action can open a new horizon.</h2>
        <p>
          Give, volunteer or partner with us to help create opportunities that
          last.
        </p>
        <div className="actions center">
          <Link className="btn light" to="/donate">
            Donate now
          </Link>
          <Link className="outline" to="/volunteer">
            Join as volunteer
          </Link>
        </div>
      </section>
    </>
  );
}
