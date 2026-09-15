import {
  LayoutDashboard,
  FolderHeart,
  CalendarDays,
  HandHeart,
  UserRound,
  LogOut,
  TrendingUp,
} from "lucide-react";
export default function Dashboard() {
  return (
    <main className="dashboard">
      <aside>
        <h2>AFAQ</h2>
        {[
          [LayoutDashboard, "Overview"],
          [FolderHeart, "Projects"],
          [HandHeart, "Donations"],
          [CalendarDays, "Events"],
          [UserRound, "Profile"],
        ].map(([I, t]) => (
          <a key={t}>
            <I size={19} />
            {t}
          </a>
        ))}
        <a className="logout">
          <LogOut size={19} />
          Logout
        </a>
      </aside>
      <section className="dash-content">
        <div className="dash-head">
          <div>
            <span className="eyebrow">MEMBER DASHBOARD</span>
            <h1>Good afternoon, Samadu.</h1>
            <p>Here's a snapshot of your Afaq activity.</p>
          </div>
          <button className="btn">Make a donation</button>
        </div>
        <div className="dash-cards">
          <article>
            <span>Total donated</span>
            <b>KSh 12,500</b>
            <small>
              <TrendingUp /> Supporting 3 projects
            </small>
          </article>
          <article>
            <span>Volunteer hours</span>
            <b>24 hrs</b>
            <small>4 activities completed</small>
          </article>
          <article>
            <span>Upcoming events</span>
            <b>3</b>
            <small>Next: Youth Skills Lab</small>
          </article>
        </div>
        <div className="dash-panel">
          <h2>Projects you support</h2>
          {[
            "Education Without Barriers",
            "Ramadan Food Support",
            "Youth Skills Lab",
          ].map((x, i) => (
            <div className="dash-project" key={x}>
              <span className="mini-icon">{i + 1}</span>
              <div>
                <b>{x}</b>
                <small>Active project</small>
              </div>
              <strong>{[72, 84, 56][i]}%</strong>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
