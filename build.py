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
    return '<ul class="news-list" aria-label="Recent news">' + "".join(
        "<li>"
        + time_value(row.get("date"))
        + ": &nbsp;"
        + link(row.get("text", ""), row.get("url", ""))
        + "</li>"
        for row in entries
    ) + "</ul>"


def render_authors(authors, owner):
    if not isinstance(authors, list):
        return text(authors)
    rendered = []
    for author in authors:
        name = author.get("name", "")
        label = f"<strong>{text(name)}</strong>" if name == owner else text(name)
        if author.get("equalContribution"):
            label += '<sup aria-label="equal contribution">#</sup>'
        rendered.append(label)
    return ", ".join(rendered) + "."


def render_publications(entries, owner="", preprint_note=True):
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
            visual = ""
        authors = (
            '<div class="pub-authors">'
            + render_authors(entry.get("authors"), owner) + "</div>"
        )
        affiliation = (
            f'<div class="pub-affiliation">{text(entry["affiliation"])}</div>'
            if entry.get("affiliation") else ""
        )
        venue_class = (
            "pub-badge pub-venue-highlight" if entry.get("venueHighlight")
            else "pub-badge"
        )
        venue = (
            f'<span class="{venue_class}">{text(entry["venue"])}</span>'
            if entry.get("venue") else ""
        )
        status = (
            f'<span class="pub-dot">{text(entry["status"])}</span>'
            if entry.get("status") else ""
        )
        resources = "".join(
            link(label, entry[key])
            for key, label in (
                ("paperUrl", "[Paper]"), ("pdfUrl", "[PDF]"),
                ("codeUrl", "[GitHub]"), ("projectUrl", "[Homepage]")
            )
            if entry.get(key)
        )
        summary = paragraphs(entry.get("summary", ""))
        rendered.append(
            '<li class="pub-item">'
            + '<div class="pub-body"><h3 class="pub-title"><strong>'
            + link(title, entry.get("paperUrl") or entry.get("projectUrl", ""))
            + "</strong></h3>"
            + authors + affiliation + summary
            + f'<div class="pub-meta">{venue}{status}{resources}</div>'
            + "</div>" + visual + "</li>"
        )
    equal_contribution = preprint_note and any(
        author.get("equalContribution")
        for entry in entries
        for author in (entry.get("authors") or [])
        if isinstance(author, dict)
    )
    note = (
        '<p class="publication-note"><sup>#</sup> for equal contribution. '
        "<em>Recent representative preprints.</em></p>"
        if equal_contribution else ""
    )
    return note + '<ul class="pub-list">' + "".join(rendered) + "</ul>"


def render_publications_by_year(entries, owner=""):
    if not entries:
        return render_publications(entries, owner, preprint_note=False)
    years = {}
    for entry in entries:
        year = str(entry.get("year") or "").strip()
        years.setdefault(year, []).append(entry)
    return "".join(
        f'<h3 class="publication-year">{text(year or "Undated")}</h3>'
        + render_publications(years[year], owner, preprint_note=False)
        for year in sorted(years, reverse=True)
    )


def split_publications(entries):
    preprints, publications = [], []
    for entry in entries:
        selected = (
            publications if entry.get("category", "preprint") == "publication"
            else preprints
        )
        selected.append(entry)
    return preprints, publications


def render_education(entries):
    if not entries:
        return '<p class="empty-state">Education details will be added here.</p>'
    rows = []
    for entry in entries:
        advisor = (
            '<p class="subtle">Advisor: '
            + link(entry["advisor"], entry.get("advisorUrl", "")) + "</p>"
            if entry.get("advisor") else ""
        )
        rows.append(
            '<li class="education-row">'
            f'<div class="entry-heading"><strong>{text(entry.get("start"))} - '
            f'{text(entry.get("end"))}</strong>'
            '<span class="entry-divider" aria-hidden="true"> | </span>'
            f'<strong>{text(entry.get("degree"))}</strong></div>'
            f'<div>{link(entry.get("school"), entry.get("url", ""))}</div>'
            f'{advisor}</li>'
        )
    return '<ul class="education-list">' + "".join(rows) + "</ul>"


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
        contact.append(
            f'<li><a class="contact-email" href="{url("mailto:" + email)}">'
            + icon("mail") + "Email</a></li>"
        )
    if profile.get("scholarUrl"):
        contact.append(
            f'<li><a href="{url(profile["scholarUrl"])}">'
            + icon("scholar") + "Google Scholar</a></li>"
        )
    if profile.get("githubUsername"):
        contact.append(
            f'<li><a href="{url("https://github.com/" + profile["githubUsername"])}">'
            + icon("github") + "GitHub</a></li>"
        )
    portrait = profile.get("portrait", "")
    if portrait:
        portrait_html = (
            f'<img class="portrait" src="{url(portrait)}" alt="{text(name)}" '
            'width="175" height="175" fetchpriority="high">'
        )
    else:
        portrait_html = (
            f'<div class="portrait profile-monogram" aria-label="{text(name)}">'
            f'<span>{text(initials)}</span></div>'
        )
    focus = "".join(f"<li>{text(value)}</li>" for value in profile.get("researchFocus", []))
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
    preprints, publications = split_publications(profile.get("publications", []))
    extras = []
    if profile.get("tools"):
        extras.append(
            f'<div id="skills"><h2>Tools &amp; Frameworks</h2><p>{tools}</p></div>'
        )
    if honors:
        extras.append(
            '<div class="honors" id="honors"><h2 id="honors-title">'
            f'Honors &amp; Awards</h2>{honors_html}</div>'
        )
    extra_section = (
        '<section class="content-section additional" id="additional">'
        + "".join(extras) + "</section>" if extras else ""
    )
    honors_nav = '<a href="#honors">Honors &amp; Awards</a>' if honors else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{text(description)}">
  <meta name="theme-color" content="#ffffff">
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
      <a class="site-name" href="#about">Homepage</a>
      <nav class="navigation" aria-label="Main navigation">
        <a href="#about" aria-current="location">About me</a>
        <a href="#news">News</a>
        <a href="#education">Education</a>
        <a href="#preprints">Selected Preprints</a>
        <a href="#publications">Selected Publications</a>
        {honors_nav}
      </nav>
    </div>
  </header>
  <div class="page-shell">
    <aside class="profile-sidebar" aria-label="Personal profile">
      <div class="profile">
        {portrait_html}
        <div class="profile-content">
          <h2 class="profile-name">{text(name)}</h2>
          <p class="profile-role">{text(profile.get("role"))}</p>
          <ul class="contact-links">{"".join(contact)}</ul>
        </div>
      </div>
    </aside>
    <main id="about-me" class="page-content">
      <section class="about-section" id="about" aria-labelledby="about-title">
        <div class="bio">
          <h1 id="about-title">About Me</h1>
          <div class="about-copy">{paragraphs(profile.get("bio", []))}</div>
          <div class="research-focus"><h2>Research Interests:</h2><ul>{focus}</ul></div>
        </div>
      </section>
      <section class="news-section" id="news" aria-labelledby="news-title">
        {heading("news", "🔥 News")}
        {render_news(profile.get("news", []))}
      </section>
      <section class="content-section" id="education" aria-labelledby="education-title">
        {heading("education", "📖 Education")}
        {render_education(profile.get("education", []))}
      </section>
      <section class="content-section" id="preprints" aria-labelledby="preprints-title">
        {heading("preprints", "📝 Selected Preprints")}
        {render_publications(preprints, name)}
      </section>
      <section class="content-section" id="publications" aria-labelledby="publications-title">
        {heading("publications", "📝 Selected Publications")}
        {render_publications_by_year(publications, name)}
      </section>
      {extra_section}
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
    markup = "\n".join(line.rstrip() for line in render(profile).splitlines()) + "\n"
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
