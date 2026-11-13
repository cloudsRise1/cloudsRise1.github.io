# Personal Homepage

Homepage: [kunzejiang.github.io](https://kunzejiang.github.io/)
 | Source repository: [kunzejiang/kunzejiang.github.io](https://github.com/kunzejiang/kunzejiang.github.io)

A standalone static homepage for GitHub Pages, using native HTML, CSS, and
JavaScript. `profile.json` stores the content, and `build.py` generates the
site using the Python standard library, with an optional `--output` argument.
No frontend framework, package manager, third-party Python packages, database,
or API key is required.

## Revision Configuration

The page is English-only. Keep all visible profile text in English and
`nameZh` empty. The current display name is `Kunze Jiang`.

The research topics must be exactly these two strings, in this order:

```json
{
  "researchFocus": ["VLM post-training", "Reinforcement learning"]
}
```

Publication records remain in the single `publications` array:

- `authors` is an array of objects with `name` and optional boolean `equalContribution`, not a single author string. The owner name is rendered in bold when an author's `name` exactly matches the top-level `name`; equal contributors receive a `#` marker.
- `category: "preprint"` selects **Selected Preprints**; `category: "publication"` selects **Selected Publications**. Published papers are grouped by `year`.
- MOD / MOD-DiT, *Mixture of Distributions Matters: Dynamic Sparse Attention for Efficient Video Diffusion Transformers*, uses `category: "publication"`, `venue: "ICML 2026"`, `venueHighlight: true`, and `year: "2026"`.
- HISD, *Hint-Informed Self-Distillation for Reasoning Segmentation*, remains `category: "preprint"`.
- **Research Experience** is no longer rendered or linked in navigation. Retain `experience: []` for configuration compatibility; adding records does not restore the section.

See [CONTENT_GUIDE.md](CONTENT_GUIDE.md) for field definitions and revision
examples. Layout inspiration is not a source of biographical facts.

## Local Preview

Python 3 is required; CI uses Python 3.12. No `pip install` or Node.js setup
is needed. From the project root:

```bash
python3 build.py
python3 -m http.server 8000
```

Open <http://localhost:8000/>. The first command uses the generator's default
output location; the second serves the current directory. Stop the server
with `Ctrl+C`.

To use a separate output directory, matching CI:

```bash
python3 build.py --output _site
python3 -m http.server 8000 --directory _site
```

`_site/` contains generated output and is ignored by Git. `.nojekyll` marks
the static site; the optional Actions workflow uploads the generated
directory without running Jekyll.

## Editing Content

Edit the supported fields in `profile.json`, then regenerate with
`python3 build.py`. For approved local assets, place files in `assets/` and
update their relative paths in the profile.

Use valid JSON without comments or trailing commas. Published content is
public: do not include passwords, tokens, private keys, or unauthorized
personal information. `.gitignore` is not a substitute for reviewing content.

## GitHub Pages

The GitHub account is `kunzejiang`, and the user-site repository is
`kunzejiang/kunzejiang.github.io`. The homepage URL is
`https://kunzejiang.github.io/`, with no repository path.

The profile records `siteUrl: "https://kunzejiang.github.io/"` and
`githubUsername: "kunzejiang"`. The generator uses these fields for the
GitHub contact link, canonical URL, Open Graph URL, structured data,
`robots.txt`, and `sitemap.xml`. Regenerate the site after updating either
field.

The local `origin` remote is
`https://github.com/kunzejiang/kunzejiang.github.io.git`.

GitHub Pages supports:

- A user site: repository `USERNAME.github.io`, URL `https://USERNAME.github.io/`.
- A project site: repository such as `personal-homepage`, URL `https://USERNAME.github.io/personal-homepage/`.
- A custom domain: the confirmed full HTTPS URL.

`USERNAME` is an example placeholder, not an instruction to rename the
account. Styles, scripts, images, and internal links should use relative
paths such as `assets/style.css`, avoiding `/assets/` for project sites.
`--output _site` selects a build directory; it does not configure a hostname
or automatically rewrite asset URLs.

The recorded deployment setup is **Settings > Pages > Deploy from a branch >
main / (root)**, publishing the generated root `index.html`. In that mode,
content updates require regenerating the page before publishing the updated
configuration and output to `main`.

An optional `.github/workflows/pages.yml` workflow supports automatic
generation from `profile.json`. To use it, the repository must contain the
workflow and **Build and deployment > Source** must be **GitHub Actions**.
Uploading a workflow with GitHub CLI requires the `workflow` scope. The
workflow builds `_site/` and deploys it to the `github-pages` environment;
it can also be triggered with **Actions > Deploy GitHub Pages > Run workflow**.
It uses `contents: read`, `pages: write`, and `id-token: write`, with deployment
concurrency group `pages` and without canceling an active deployment.

Pages publishes from `main` at the repository root, with HTTPS enabled and
no custom-domain CNAME. The `kunzejiang.github.io` address comes from the
account and repository names.
