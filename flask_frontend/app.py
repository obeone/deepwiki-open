from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

API_URL = os.environ.get("DEEPWIKI_API_URL", "http://localhost:8001")
PORT = int(os.environ.get("DEEPWIKI_FRONTEND_PORT", "5000"))


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the home page and handle project submission.

    Returns:
        str: Rendered HTML for the page.
    """
    if request.method == "POST":
        repo_url = request.form.get("repo_url", "").strip()
        repo_type = request.form.get("repo_type", "github")
        token = request.form.get("token", "").strip()
        params = {
            "repo_url": repo_url,
            "token": token,
            "repo_type": repo_type,
        }
        try:
            requests.post(
                f"{API_URL}/api/processed_projects",
                json=params,
                timeout=10,
            )
        except Exception:
            pass
        return redirect(url_for("projects"))
    return render_template("index.html")


@app.route("/projects")
def projects():
    """
    Display processed projects retrieved from the backend API.

    Returns:
        str: Rendered HTML listing processed projects.
    """
    try:
        response = requests.get(f"{API_URL}/api/processed_projects", timeout=10)
        response.raise_for_status()
        projects = response.json()
    except Exception:
        projects = []
    return render_template("projects.html", projects=projects)


@app.route("/projects/<repo_type>/<owner>/<repo>/<language>")
def project_detail(repo_type: str, owner: str, repo: str, language: str):
    """
    Display details for a single processed project.

    Args:
        repo_type (str): Repository type like github.
        owner (str): Repository owner.
        repo (str): Repository name.
        language (str): Language of the wiki.

    Returns:
        str: Rendered HTML showing project details.
    """
    params = {
        "owner": owner,
        "repo": repo,
        "repo_type": repo_type,
        "language": language,
    }
    try:
        response = requests.get(f"{API_URL}/api/wiki_cache", params=params, timeout=10)
        response.raise_for_status()
        project = response.json()
    except Exception:
        project = None
    return render_template("project_detail.html", project=project)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
