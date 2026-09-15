const API_URL = "http://127.0.0.1:5000/api";


export async function getProjects() {
  const response = await fetch(`${API_URL}/projects`);

  if (!response.ok) {
    throw new Error("Failed to load projects.");
  }

  const data = await response.json();

  return data;
}


export async function getProject(projectId) {
  const response = await fetch(
    `${API_URL}/projects/${projectId}`
  );

  if (!response.ok) {
    throw new Error("Project not found.");
  }

  return response.json();
}
