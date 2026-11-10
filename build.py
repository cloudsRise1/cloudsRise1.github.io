#!/usr/bin/env python3
"""Build a portable, dependency-free GitHub Pages research homepage."""

import argparse
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent


def text(value):
    return html.escape(str(value or ""), quote=True)


def url(value):
    """Only permit normal web/contact links or portable local asset paths."""
    value = str(value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    if parsed.scheme in ("https", "http") and parsed.netloc:
        return text(value)
    if parsed.scheme == "mailto" and parsed.path:
        return text(value)
    if not parsed.scheme and not value.startswith(("/", "\\")):
        if ".." not in Path(parsed.path).parts and "\\" not in value:
            return text(value)
    raise ValueError(f"Unsupported or non-portable URL: {value}")


def link(label, href, class_name=""):
    if not href:
        return text(label)
    attr = f' class="{text(class_name)}"' if class_name else ""
    return f'<a{attr} href="{url(href)}">{text(label)}</a>'


def icon(name):
    return (
        '<svg class="inline-icon" width="16" height="16" aria-hidden="true">'
        f'<use href="./assets/icons.svg#{text(name)}"></use></svg>'
    )


def paragraphs(values):
    if isinstance(values, str):
        values = [values]
    return "".join(f"<p>{text(value)}</p>" for value in values if value)


def heading(identifier, title):
    return (
        '<div class="section-heading">'
        f'<h2 id="{identifier}-title">{text(title)}</h2></div>'
    )


def time_value(value):
    value = str(value or "")
    if re.fullmatch(r"\d{4}([.-]\d{2}){0,2}", value):
        return f'<time datetime="{value.replace(".", "-")}">{text(value)}</time>'
    return f'<span class="news-date">{text(value)}</span>'


def render_news(entries):
    if not entries:
        return '<p class="empty-state">Research updates will be shared here.</p>'

    def items(rows):
        return '<ul class="news-list">' + "".join(
            "<li>"
            + time_value(row.get("date"))
            + "<span>"
            + link(row.get("text", ""), row.get("url", ""))
            + "</span></li>"
            for row in rows
        ) + "</ul>"

    result = items(entries[:3])
    if len(entries) > 3:
        result += (
            '<details class="earlier-news"><summary>Earlier updates</summary>'
            + items(entries[3:])
            + "</details>"
        )
    return result


def render_publications(entries):
    if not entries:
        return (
            '<p class="empty-state">A selected list of papers and open-source '
            "projects will be added here.</p>"
        )
    rendered = []
    for entry in entries:
        title = entry.get("title", "")
        figure = entry.get("figure", "")
        caption = entry.get("figureCaption", "") or title
        if figure:
            figure_url = url(figure)
            visual = (
                f'<button class="pub-teaser" type="button" data-figure="{figure_url}" '
                f'data-caption="{text(caption)}" aria-label="Enlarge figure: {text(caption)}">'
                f'<img src="{figure_url}" alt="{text(caption)}" '
                'width="520" height="300" loading="lazy" decoding="async"></button>'
            )
        else:
            visual = (
                '<div class="pub-placeholder" aria-hidden="true">'
                f'<span>{text(entry.get("venue") or "Research")}</span>'
                f'<strong>{text(entry.get("shortTitle") or title.split(":")[0])}</strong>'
                "</div>"
            )
        role = (
            f'<span class="pub-role">{text(entry["role"])}</span>'
            if entry.get("role") else ""
        )
        authors = f'<div class="pub-authors">{text(entry.get("authors"))} {role}</div>'
        affiliation = (
            f'<div class="pub-affiliation">{text(entry["affiliation"])}</div>'
            if entry.get("affiliation") else ""
        )
        venue = (
            f'<span class="pub-badge">{text(entry["venue"])}</span>'
            if entry.get("venue") else ""
        )
        status = (
            f'<span class="pub-dot">{text(entry["status"])}</span>'
            if entry.get("status") else ""
        )
        resources = "".join(
            link(label, entry[key])
            for key, label in (
                ("paperUrl", "paper"), ("codeUrl", "code"), ("projectUrl", "project")
            )
            if entry.get(key)
        )
        summary = paragraphs(entry.get("summary", ""))
        rendered.append(
            '<article class="pub-item">'
            + visual
            + '<div class="pub-body"><h3 class="pub-title">'
            + link(title, entry.get("paperUrl") or entry.get("projectUrl", ""))
            + "</h3>"
            + authors + affiliation + summary
            + f'<div class="pub-meta">{venue}{status}{resources}</div>'
            + "</div></article>"
        )
    return '<div class="pub-list">' + "".join(rendered) + "</div>"


def render_experience(entries):
    if not entries:
        return '<p class="empty-state">Professional and research experience will be added here.</p>'
    rows = []
    for entry in entries:
        company = entry.get("company", "")
        initials = "".join(word[0] for word in company.split()[:2] if word).upper()
        rows.append(
            '<article class="internship-card">'
            f'<div class="internship-logo company-monogram" aria-hidden="true">{text(initials)}</div>'
            '<div class="internship-body"><div class="internship-head"><div>'
            f'<h3 class="internship-company">{link(company, entry.get("url", ""))}</h3>'
            f'<div class="internship-role">{text(entry.get("role"))}</div></div>'
            f'<div class="internship-time">{text(entry.get("start"))} — '
            f'{text(entry.get("end") or "Present")}</div></div>'
            + paragraphs(entry.get("description", []))
            + "</div></article>"
        )
    return '<div class="internship-list">' + "".join(rows) + "</div>"


def render_education(entries):
    if not entries:
        return '<p class="empty-state">Education details will be added here.</p>'
    rows = []
    for entry in entries:
        advisor = (
            '<p class="subtle">Advisor · '
            + link(entry["advisor"], entry.get("advisorUrl", "")) + "</p>"
            if entry.get("advisor") else ""
        )
        rows.append(
            '<article class="education-row">'
            f'<div class="education-date">{text(entry.get("start"))} — '
            f'{text(entry.get("end"))}</div><div>'
            f'<h3>{link(entry.get("school"), entry.get("url", ""))}</h3>'
            f'<p>{text(entry.get("degree"))}</p>{advisor}</div></article>'
        )
    return "".join(rows)


def render(profile):
    name = profile.get("name") or "Your Name"
    initials = profile.get("initials") or "".join(w[0] for w in name.split()[:2])
    description = profile.get("description") or f"{name} — research and projects."
    site_url = str(profile.get("siteUrl") or "").strip().rstrip("/") + "/"
    has_site_url = site_url != "/"
    metadata = (
        f'  <link rel="canonical" href="{url(site_url)}">\n'
        f'  <meta property="og:url" content="{url(site_url)}">\n'
        if has_site_url else ""
    )
    if has_site_url:
        schema = {
            "@context": "https://schema.org", "@type": "Person",
            "name": name, "url": site_url, "description": description,
        }
        same_as = []
        if profile.get("githubUsername"):
            same_as.append("https://github.com/" + profile["githubUsername"])
        if profile.get("scholarUrl"):
            same_as.append(profile["scholarUrl"])
        if same_as:
            schema["sameAs"] = same_as
        # Escape '<' so user-authored strings cannot end the script element.
        schema_json = json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")
        metadata += f'  <script type="application/ld+json">{schema_json}</script>\n'
    contact = []
    email = str(profile.get("email") or "")
    if email:
        contact.append(link(email, "mailto:" + email, "contact-email"))
    socials = []
    if profile.get("scholarUrl"):
        socials.append(link("Google Scholar", profile["scholarUrl"]))
    if profile.get("githubUsername"):
        socials.append(
            link("GitHub ↗", "https://github.com/" + profile["githubUsername"])
        )
    if socials:
        contact.append(
            '<p class="contact-links">'
            + '<span aria-hidden="true">·</span>'.join(socials) + "</p>"
        )
    portrait = profile.get("portrait", "")
    if portrait:
        portrait_html = (
            f'<img class="portrait" src="{url(portrait)}" alt="{text(name)}" '
            'width="220" height="220" fetchpriority="high">'
        )
    else:
        portrait_html = (
            f'<div class="portrait profile-monogram" aria-label="{text(name)}">'
            f'<span>{text(initials)}</span><small>RESEARCH &amp; EXPLORATION</small></div>'
        )
    focus = "".join(f"<li>{text(value)}</li>" for value in profile.get("researchFocus", []))
    interests = "".join(f"<li>{text(value)}</li>" for value in profile.get("interests", []))
    tools = (
        text(" · ".join(profile.get("tools", [])))
        or '<span class="subtle">Selected tools and frameworks will be added here.</span>'
    )
    honors = profile.get("honors", [])
    honors_html = (
        "<ul>" + "".join(
            f'<li>{text(row.get("name"))} <span>({text(row.get("year"))})</span></li>'
            for row in honors
        ) + "</ul>"
        if honors else '<p class="empty-state">Selected honors will be added here.</p>'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{text(description)}">
  <meta name="theme-color" content="#fbfaf7">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{text(name)} — Research">
  <meta property="og:description" content="{text(description)}">
  <meta name="twitter:card" content="summary">
{metadata}  <title>{text(name)} — Research</title>
  <link rel="stylesheet" href="./assets/style.css">
  <script src="./assets/app.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#about">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="site-name" href="#about"><span class="personal-name">{text(name)}</span></a>
      <nav class="navigation" aria-label="Main navigation">
        <a href="#about" aria-current="location">About</a>
        <a href="#news">News</a>
        <a href="#publications">Publications</a>
        <a href="#internships">Experience</a>
        <a href="#education">Education</a>
      </nav>
    </div>
  </header>
  <div class="page-shell">
    <main id="about-me">
      <section class="about-section" id="about" aria-labelledby="about-title">
        <div class="profile">
          {portrait_html}
          <div class="profile-contact">{"".join(contact)}</div>
        </div>
        <div class="bio">
          <h1 id="about-title">Hi, I'm <em class="personal-name">{text(name)}</em>.</h1>
          <p class="profile-role">{text(profile.get("role"))}</p>
          <div class="about-copy">{paragraphs(profile.get("bio", []))}</div>
          <div class="research-focus"><h2>Research focus</h2><ul>{focus}</ul></div>
        </div>
      </section>
      <section class="news-section" id="news" aria-labelledby="news-title">
        {heading("news", "News & timeline")}
        {render_news(profile.get("news", []))}
      </section>
      <section class="content-section" id="publications" aria-labelledby="publications-title">
        {heading("publications", "Publications")}
        {render_publications(profile.get("publications", []))}
      </section>
      <section class="content-section" id="internships" aria-labelledby="internships-title">
        {heading("internships", "Experience")}
        {render_experience(profile.get("experience", []))}
      </section>
      <section class="content-section" id="education" aria-labelledby="education-title">
        {heading("education", "Education")}
        {render_education(profile.get("education", []))}
      </section>
      <section class="content-section additional" id="additional" aria-label="Research interests, tools, and honors">
        <div id="interests"><h2>Research interests</h2><ul>{interests}</ul></div>
        <div id="skills"><h2>Tools &amp; frameworks</h2><p>{tools}</p>
          <p class="subtle">From research ideas to reproducible systems.</p></div>
        <div class="honors" id="honors"><h2>Honors</h2>{honors_html}</div>
      </section>
      <footer><span class="personal-name">{text(name)} <span class="subtle">© <span data-current-year>{date.today().year}</span></span></span>
        <a href="#about">Back to top ↑</a></footer>
    </main>
  </div>
  <dialog class="figure-dialog" aria-labelledby="figure-title">
    <div class="figure-toolbar"><h2 id="figure-title">Research figure</h2>
      <button class="close-figure" type="button" aria-label="Close figure">×</button></div>
    <img class="figure-image" alt="">
    <p class="figure-caption"></p>
  </dialog>
</body>
</html>
"""


def validate_profile(profile):
    if not isinstance(profile, dict):
        raise ValueError("profile.json must contain an object.")
    for field in ("bio", "researchFocus", "news", "publications", "experience",
                  "education", "interests", "tools", "honors"):
        if field in profile and not isinstance(profile[field], list):
            raise ValueError(f"profile.{field} must be an array.")
    username = profile.get("githubUsername", "")
    if username and not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", username):
        raise ValueError("githubUsername must be a valid GitHub username.")
    for field in ("name", "nameZh", "initials", "role", "description", "email",
                  "siteUrl", "portrait", "scholarUrl", "githubUsername"):
        if field in profile and not isinstance(profile[field], str):
            raise ValueError(f"profile.{field} must be a string.")
    for field in ("bio", "researchFocus", "interests", "tools"):
        if any(not isinstance(item, str) for item in profile.get(field, [])):
            raise ValueError(f"profile.{field} must contain strings.")
    for field in ("news", "publications", "experience", "education", "honors"):
        if any(not isinstance(item, dict) for item in profile.get(field, [])):
            raise ValueError(f"profile.{field} must contain objects.")
    site_url = profile.get("siteUrl", "")
    if site_url and urlparse(site_url).scheme not in ("http", "https"):
        raise ValueError("siteUrl must be an absolute https:// or http:// URL.")


def build(output):
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    validate_profile(profile)
    markup = render(profile)
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(markup, encoding="utf-8")
    if output.resolve() != ROOT:
        shutil.copytree(ROOT / "assets", output / "assets", dirs_exist_ok=True)
        for name in ("404.html", ".nojekyll"):
            if (ROOT / name).exists():
                shutil.copy2(ROOT / name, output / name)
    site_url = profile.get("siteUrl", "").rstrip("/")
    # Only emit search-engine location metadata once the real URL is known.
    if site_url:
        sitemap = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{xml_escape(site_url + '/')}</loc></url></urlset>\n"
        )
        (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
        (output / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: " + site_url + "/sitemap.xml\n",
            encoding="utf-8",
        )
    else:
        for filename in ("sitemap.xml", "robots.txt"):
            stale = output / filename
            if stale.exists():
                stale.unlink()
    print(f"Built {output / 'index.html'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT,
        help="Output directory (default: directory containing build.py)",
    )
    args = parser.parse_args()
    build(args.output.resolve())
