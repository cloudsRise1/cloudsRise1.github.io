# Homepage Content Guide

## Scope And Revision

Edit `profile.json` to supply homepage content and use `build.py` to generate
the page, as described in [README.md](README.md). The page is English-only:
use English for visible content and keep `nameZh` empty. The current display
name is `Kunze Jiang`, with initials `KJ`; the old identity placeholders are
not the current configuration.

`researchFocus` must be exactly `["VLM post-training", "Reinforcement learning"]`,
preserving spelling, capitalization, and order. Do not add other topics.

Use author objects and explicit publication categories. **Selected Preprints**
and **Selected Publications** are separate rendered sections, both populated
from `publications`. **Research Experience** is no longer rendered or linked
in navigation; retain `experience: []` for compatibility.

Add only user-confirmed content. Do not infer institutions, jobs, degrees,
advisors, authorship, publication status, honors, or quantitative results.
Reference homepages supply layout inspiration, not the owner's biography.

This revision edits only `README.md` and `CONTENT_GUIDE.md`. Other agents own
`build.py`, `profile.json`, CSS, and ephemeral QA; the main agent owns namespace
investigation and deployment decisions. No builds, tests, commits, pushes,
browser actions, or edits to those implementation files are part of this
documentation task.

## JSON Rules

- Use valid JSON with double-quoted keys and strings, without comments or trailing commas.
- Retain the existing top-level keys for compatibility.
- Use `""` for unknown text and `[]` for empty lists.
- Omit optional record fields when unknown, or leave optional text as `""`.
- Treat text as plain text; do not insert HTML or Markdown to bold the owner name. The generator applies author formatting.
- Keep records in the intended display order; newest-first is recommended for dated lists.
- Use the revision fragment only for the documented fields; preserve the rest of the confirmed profile.

## Top-Level Schema

These are the profile's content fields. Empty strings and arrays are
intentional where information is absent.

| Key | Type | Meaning |
| --- | --- | --- |
| `name` | string | Confirmed display name, currently `Kunze Jiang`; also used for exact author-name matching. |
| `nameZh` | string | Keep `""` for this English-only revision. |
| `initials` | string | Display initials, currently `KJ`. |
| `role` | string | Confirmed English profile label. |
| `githubUsername` | string | Actual GitHub profile owner, without `@` or a URL; not a requested hostname. |
| `email` | string | Confirmed public contact email, without `mailto:`. |
| `scholarUrl` | string | Confirmed Google Scholar profile URL. |
| `description` | string | Short English site description. |
| `bio` | string[] | Biography paragraphs, one plain-text string per paragraph. |
| `researchFocus` | string[] | Exactly `["VLM post-training", "Reinforcement learning"]`, in this order. |
| `news` | object[] | Updates using the news schema below. |
| `publications` | object[] | Paper records, split into preprints and publications by `category`. |
| `experience` | object[] | Compatibility-only data; keep `[]`. Research Experience is not rendered. |
| `education` | object[] | Confirmed education records. |
| `interests` | string[] | Retained user-supplied interests; not a replacement for `researchFocus`. |
| `tools` | string[] | User-confirmed tools; empty if absent. |
| `honors` | object[] | Confirmed honors. |
| `siteUrl` | string | Full canonical URL of the actual published host, including any project path; not a proposed destination. |
| `portrait` | string, optional | Relative path to an approved local portrait asset. |

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
| `authors` | object[] | Ordered author objects using the schema below; do not use a single display string. |
| `category` | string | Exactly `preprint` or `publication`; controls the rendered section. |
| `venue` | string | Verified venue or preprint source; empty when unknown. |
| `venueHighlight` | boolean, optional | Highlights the venue label when `true`; MOD uses `true`. |
| `year` | string, optional | Year heading for Selected Publications; MOD uses `"2026"`. Supply a four-digit year for dated publications. |
| `status` | string, optional | Additional verified status text; does not replace `category` or determine the section. |
| `affiliation` | string, optional | Confirmed affiliation associated with the work. |
| `summary` | string, optional | Factual summary without unsupported results or metrics. |
| `paperUrl` | string, optional | Verified paper URL. |
| `pdfUrl` | string, optional | Verified direct PDF URL. |
| `codeUrl` | string, optional | Verified code URL. |
| `projectUrl` | string, optional | Verified project URL. |
| `figure` | string, optional | Path to a user-provided local figure approved for publication. No external images, placeholders, or guessed assets. |
| `figureCaption` | string, optional | English caption for the figure; the title is used when omitted. |

#### Authors

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string | Exact author name, preserving verified author order. |
| `equalContribution` | boolean, optional | `true` adds the `#` equal-contribution marker; omitted or `false` means no marker. |

The owner's author name is bold only when it exactly equals the top-level
`name` (`Kunze Jiang` in this revision). Keep the stored name plain text, with
no Markdown, HTML, or manually appended contribution marker.

`category: "preprint"` renders under **Selected Preprints**.
`category: "publication"` renders under **Selected Publications**, grouped
by `year` newest-first. Keep both kinds in the same `publications` array;
do not introduce separate top-level arrays or use `status` for routing.

### Experience

This schema is retained only for legacy configuration compatibility. The
revision keeps `experience: []`; even populated records do not render a
Research Experience section.

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
| `url` | string, optional | Verified institution URL. |
| `advisor` | string, optional | Confirmed advisor name. |
| `advisorUrl` | string, optional | Verified advisor profile URL. |

### Honors

| Field | Type | Meaning |
| --- | --- | --- |
| `name` | string | Exact confirmed honor or award name. |
| `year` | string | Confirmed year, preferably `YYYY`. |

## Revision Configuration

This fragment documents the revised research topics, author format, and
paper classification. It is not a complete replacement for `profile.json`;
preserve the remaining profile fields and confirmed resource links.

```json
{
  "name": "Kunze Jiang",
  "nameZh": "",
  "researchFocus": ["VLM post-training", "Reinforcement learning"],
  "publications": [
    {
      "title": "Hint-Informed Self-Distillation for Reasoning Segmentation",
      "authors": [
        {"name": "Kunze Jiang", "equalContribution": true},
        {"name": "Yuchen Wang", "equalContribution": true},
        {"name": "Kang Li"},
        {"name": "Qixing Zhang"}
      ],
      "category": "preprint",
      "venue": "arXiv preprint, 2026"
    },
    {
      "title": "Mixture of Distributions Matters: Dynamic Sparse Attention for Efficient Video Diffusion Transformers",
      "authors": [
        {"name": "Yuxi Liu"},
        {"name": "Yipeng Hu"},
        {"name": "Zekun Zhang"},
        {"name": "Kunze Jiang"},
        {"name": "Kun Yuan"}
      ],
      "category": "publication",
      "venue": "ICML 2026",
      "venueHighlight": true,
      "year": "2026"
    }
  ],
  "experience": []
}
```

## GitHub Pages Content

The confirmed GitHub account is `kunzejiang`, the repository is
`kunzejiang/kunzejiang.github.io`, and the homepage is
`https://kunzejiang.github.io/`.

The profile records:

```json
{
  "githubUsername": "kunzejiang",
  "siteUrl": "https://kunzejiang.github.io/"
}
```

`siteUrl` supplies the canonical URL, Open Graph URL, structured data,
`robots.txt`, and `sitemap.xml`. `githubUsername` supplies the GitHub contact
link and the GitHub profile URL in structured data. Keep both fields aligned
with the account and published host, and regenerate the site after changing
them. For a new profile with no confirmed destination, leave unknown values
empty rather than guessing.

- For a user site, the usual repository is `<username>.github.io` and the usual `siteUrl` is `https://<username>.github.io/`.
- For a project site, the usual `siteUrl` is `https://<username>.github.io/<repository>/`, including the repository path.
- For a custom domain, use the confirmed full HTTPS URL instead.
- Replace angle-bracket placeholders only with confirmed values. Do not use these literal example URLs in the profile.
- `siteUrl` supplies canonical/search metadata, not deployment configuration. Changing it does not migrate the site or configure GitHub Pages.
- `--output _site` selects only the output directory; it does not establish a publishing namespace.
- Empty contact fields produce no contact links. Empty lists must not introduce fabricated biographical records.

## Before Publishing

- Keep visible content English-only and `nameZh` empty.
- Preserve the exact two-entry `researchFocus` array.
- Check author order, exact owner-name matching, and equal-contribution flags.
- Keep HISD as a preprint and MOD as a publication with `venue: "ICML 2026"`, `venueHighlight: true`, and `year: "2026"`.
- Do not expect Research Experience to appear; keep `experience: []`.
- Verify each added record and all public contact details.
- Confirm permission and provenance for any local figure.
- Validate the JSON and regenerate/preview with `build.py` before publishing.
- Check `siteUrl` against the published host and `githubUsername` against the actual profile owner.
- Remove all illustrative placeholder records from publishable content.
