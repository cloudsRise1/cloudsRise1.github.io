# Homepage Content Guide

## Scope And Defaults

Edit `profile.json` to supply homepage content. The reference homepage at
https://sansanyuchen.github.io is visual inspiration only. Its owner, Wang
Yuchen, is not assumed to be the user; none of its biographical details should
be copied as user facts.

Identity is awaiting user confirmation. `Your Name`, `YN`, and
`LLM & Multimodal Research` are editable English defaults. The description,
bio, and research topics are drafts based on the supplied research context,
not verified credentials or achievements. Review them before publishing.

Contact fields and `siteUrl` remain empty. News, publications, experience,
education, interests, tools, and honors start as empty arrays. Add only
user-confirmed content. Do not infer institutions, jobs, degrees, advisors,
authorship, publication status, honors, or quantitative results.

This guide and `profile.json` contain content only. The main agent owns the
generator, rendering behavior, and GitHub Pages setup. No generator changes,
commits, repository creation, or remote deployment actions are part of these
files.

## JSON Rules

- Use valid JSON with double-quoted keys and strings, without comments or trailing commas.
- Keep the top-level keys listed below.
- Use `""` for unknown text and `[]` for empty lists.
- Omit optional record fields when unknown, or leave optional text as `""`.
- Treat text as plain text unless the generator explicitly supports formatting.
- Keep records in the intended display order; newest-first is recommended for dated lists.
- Do not paste the illustrative examples into a published profile as facts.

## Top-Level Schema

All top-level keys are required. Empty strings and arrays are intentional.

| Key | Type | Meaning |
| --- | --- | --- |
| `name` | string | Confirmed display name; default `Your Name`. |
| `nameZh` | string | Optional Chinese display name; empty until supplied. |
| `initials` | string | Display initials; default `YN`. |
| `role` | string | Editable research label; default `LLM & Multimodal Research`, not an employment claim. |
| `githubUsername` | string | Confirmed GitHub username only, without `@` or a URL. |
| `email` | string | Confirmed public contact email, without `mailto:`. |
| `scholarUrl` | string | Confirmed Google Scholar profile URL. |
| `description` | string | Short site description; current wording is a research-interest draft. |
| `bio` | string[] | Biography paragraphs, one plain-text string per paragraph. |
| `researchFocus` | string[] | Research topic labels. |
| `news` | object[] | Updates using the news schema below. |
| `publications` | object[] | Verified publication records using the publication schema below. |
| `experience` | object[] | Confirmed experience records. |
| `education` | object[] | Confirmed education records. |
| `interests` | string[] | User-supplied interests; initially empty. |
| `tools` | string[] | User-confirmed tools; initially empty. |
| `honors` | object[] | Confirmed honors. |
| `siteUrl` | string | Full canonical homepage URL after its destination is confirmed. |

## Record Schemas

Fields are required within each record unless marked optional. Dates and
years are strings so the user can preserve the appropriate precision.

### News

| Field | Type | Meaning |
| --- | --- | --- |
| `date` | string | Update date, preferably `YYYY-MM-DD` or `YYYY-MM`. |
| `text` | string | User-confirmed update text. |
| `url` | string, optional | Supporting link. |
| `label` | string, optional | Short category label. |

### Publications

| Field | Type | Meaning |
| --- | --- | --- |
| `title` | string | Exact verified paper title. |
| `authors` | string | Author list as one display string, preserving verified author order. |
| `venue` | string | Verified venue or preprint source; empty when unknown. |
| `status` | string | Verified status, such as preprint or published; do not imply acceptance without confirmation. |
| `role` | string, optional | Confirmed contribution or authorship note. |
| `affiliation` | string, optional | Confirmed affiliation associated with the work. |
| `summary` | string, optional | Factual summary without unsupported results or metrics. |
| `paperUrl` | string, optional | Verified paper URL. |
| `codeUrl` | string, optional | Verified code URL. |
| `projectUrl` | string, optional | Verified project URL. |
| `figure` | string, optional | Path to a user-provided local figure approved for publication. No external images, placeholders, or guessed assets. |

### Experience

| Field | Type | Meaning |
| --- | --- | --- |
| `company` | string | Confirmed organization name. |
| `role` | string | Confirmed position or appointment. |
| `start` | string | Start date, preferably `YYYY-MM` or `YYYY`. |
| `end` | string | End date; `Present` only for a confirmed current role. |
| `description` | string[] | Separate factual responsibility or contribution statements. |

### Education

| Field | Type | Meaning |
| --- | --- | --- |
| `school` | string | Confirmed institution name. |
| `degree` | string | Confirmed degree or program; distinguish enrollment from an awarded degree. |
| `start` | string | Start date, preferably `YYYY-MM` or `YYYY`. |
| `end` | string | End date or confirmed current enrollment status; label expected dates explicitly. |
| `advisor` | string, optional | Confirmed advisor name. |
| `advisorUrl` | string, optional | Verified advisor profile URL. |

### Honors

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string | Exact confirmed honor or award name. |
| `year` | string | Confirmed year, preferably `YYYY`. |

## Illustrative Records Only

The following fragment demonstrates record shapes, not the user's history.
Every example is an illustrative placeholder. It is not a complete profile,
must not be published unchanged, and is deliberately absent from
`profile.json`. Blank links and dates demonstrate unknown values.

```json
{
  "news": [
    {
      "date": "",
      "text": "Illustrative placeholder: replace with a confirmed update.",
      "url": "",
      "label": "Illustrative example"
    }
  ],
  "publications": [
    {
      "title": "Illustrative placeholder: verified paper title",
      "authors": "Illustrative placeholder: verified author list",
      "venue": "",
      "status": "",
      "role": "",
      "affiliation": "",
      "summary": "Illustrative placeholder: factual paper summary.",
      "paperUrl": "",
      "codeUrl": "",
      "projectUrl": "",
      "figure": ""
    }
  ],
  "experience": [
    {
      "company": "Illustrative placeholder: confirmed organization",
      "role": "Illustrative placeholder: confirmed position",
      "start": "",
      "end": "",
      "description": [
        "Illustrative placeholder: confirmed responsibility."
      ]
    }
  ],
  "education": [
    {
      "school": "Illustrative placeholder: confirmed institution",
      "degree": "Illustrative placeholder: confirmed degree or program",
      "start": "",
      "end": "",
      "advisor": "",
      "advisorUrl": ""
    }
  ],
  "honors": [
    {
      "name": "Illustrative placeholder: confirmed honor",
      "year": ""
    }
  ]
}
```

## GitHub Pages Content

Leave `githubUsername` and `siteUrl` empty until the user confirms the account
and publishing destination. The reference site's username is not a default.

- For a user site, the usual repository is `<username>.github.io` and the usual `siteUrl` is `https://<username>.github.io/`.
- For a project site, the usual `siteUrl` is `https://<username>.github.io/<repository>/`, including the repository path.
- For a custom domain, use the confirmed full HTTPS URL instead.
- Replace angle-bracket placeholders only with confirmed values. Do not use these literal example URLs in the profile.
- `siteUrl` is content metadata, not deployment configuration. The generator must separately handle the Pages base path and local asset links.
- Empty contact fields should produce no contact links, and empty lists should produce no fabricated entries; the generator must implement this behavior.

## Before Publishing

- Confirm the name, initials, optional Chinese name, and research label with the user.
- Obtain approval for the draft description, bio, and research topics.
- Verify each added record and all public contact details.
- Confirm permission and provenance for any local figure.
- Validate the JSON after editing and preview using the main agent's generator.
- Check canonical URL and asset paths against the selected GitHub Pages destination.
- Remove all illustrative placeholder records from publishable content.
