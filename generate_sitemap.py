import os
import subprocess
from datetime import datetime

# Change this if you ever switch to a custom domain
BASE_URL = "https://vishal-1708.github.io/digital-flow"

EXCLUDE_DIRS = {".git", ".github"}
EXCLUDE_FILES = {"404.html"}

def get_last_modified(filepath):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=short", "--", filepath],
            capture_output=True, text=True, check=True
        )
        date = result.stdout.strip()
        return date if date else datetime.today().strftime("%Y-%m-%d")
    except Exception:
        return datetime.today().strftime("%Y-%m-%d")

def find_html_files():
    html_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".html") and f not in EXCLUDE_FILES:
                path = os.path.relpath(os.path.join(root, f), ".")
                html_files.append(path.replace("\\", "/"))
    return sorted(html_files)

def priority_for(path):
    if path == "index.html":
        return "1.0"
    if path == "blog.html":
        return "0.8"
    if path.startswith("blog-post"):
        return "0.7"
    if path == "contact.html":
        return "0.5"
    return "0.6"

def changefreq_for(path):
    if path == "blog.html":
        return "weekly"
    if path == "contact.html":
        return "yearly"
    return "monthly"

def build_sitemap():
    files = find_html_files()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in files:
        loc = f"{BASE_URL}/{f}"
        lastmod = get_last_modified(f)
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq_for(f)}</changefreq>")
        lines.append(f"    <priority>{priority_for(f)}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open("sitemap.xml", "w") as out:
        out.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    build_sitemap()
