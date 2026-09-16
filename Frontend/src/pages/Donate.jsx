import { Link, useSearchParams } from "react-router-dom";

export default function Donate() {
  const [searchParams] = useSearchParams();

  const projectId = searchParams.get("project");

  return (
    <main className="simple">
      <span className="eyebrow">
        AFAQ FOUNDATION
      </span>

      <h1>Support a project</h1>

      <p>
        Your contribution helps Afaq Foundation
        support communities and create measurable impact.
      </p>

      {projectId && (
        <p>
          Selected project ID: <b>{projectId}</b>
        </p>
      )}

      <Link className="btn" to="/projects">
        View projects
      </Link>
    </main>
  );
}