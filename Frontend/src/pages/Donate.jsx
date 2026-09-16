import { useEffect, useState } from "react";
import {
  Link,
  useSearchParams,
} from "react-router-dom";

import {
  ArrowLeft,
  MapPin,
  Users,
} from "lucide-react";

import { getProject } from "../services/projectsApi";


const money = (n = 0) =>
  "KSh " + Number(n).toLocaleString();


export default function Donate() {
  const [searchParams] = useSearchParams();

  const projectId = searchParams.get("project");

  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    async function loadProject() {
      if (!projectId) {
        setError("No project was selected.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);

        const data = await getProject(projectId);

        setProject({
          id: data.id,
          title: data.title,
          summary:
            data.summary || data.description,
          category: data.category,
          location: data.location,
          beneficiaries: data.beneficiaries,
          icon: data.icon,
          target: data.target_amount,
          raised: data.amount_raised,
          status: data.status,
        });

        setError("");
      } catch (err) {
        console.error(err);

        setError(
          "Unable to load the selected project."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProject();
  }, [projectId]);


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
        <span className="eyebrow">
          AFAQ FOUNDATION
        </span>

        <h1>Project unavailable</h1>

        <p>{error}</p>

        <Link
          className="btn"
          to="/projects"
        >
          View projects
        </Link>
      </main>
    );
  }


  const remaining = Math.max(
    0,
    project.target - project.raised
  );


  return (
    <main className="simple">

      <Link
        className="back"
        to={"/projects/" + project.id}
      >
        <ArrowLeft size={17} />
        Back to project
      </Link>


      <span className="eyebrow">
        SUPPORT AFAQ
      </span>


      <div
        style={{
          fontSize: "70px",
          marginTop: "20px",
        }}
      >
        {project.icon}
      </div>


      <h1>
        Support {project.title}
      </h1>


      <p>
        {project.summary}
      </p>


      <div className="detail-meta">

        <span>
          <MapPin size={17} />
          {project.location}
        </span>

        <span>
          <Users size={17} />
          {project.beneficiaries} beneficiaries
        </span>

      </div>


      <div
        style={{
          marginTop: "30px",
          marginBottom: "30px",
        }}
      >
        <p>
          <strong>
            {money(project.raised)}
          </strong>{" "}
          raised of {money(project.target)}
        </p>

        <p>
          {money(remaining)} remaining
        </p>
      </div>


      <h2>
        Make a contribution
      </h2>

      <p>
        Donation form coming next.
      </p>

    </main>
  );
}
