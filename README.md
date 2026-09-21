# Flavio Martins — CV website

Live site: [engflaviomartins.github.io](https://engflaviomartins.github.io/)

This is a static HTML/CSS/JavaScript website. GitHub Pages publishes the root of the `main` branch; there is no build step or paid hosting service.

## Update the site

For small changes, open the relevant file on GitHub, choose **Edit**, then commit the change to `main`. GitHub Pages republishes automatically after each push.

| Content | File |
| --- | --- |
| Home page and illustrated research summaries | `index.html` |
| Professional and academic HTML CVs | `cv/index.html` |
| Publication list | `assets/publications.js` |
| Projects and GitHub links | `projects/index.html` |
| Design and phone layout | `assets/styles.css` |
| Downloadable CV PDFs | `downloads/` |
| Research illustrations | `assets/work/` |

The publication list is curated in `assets/publications.js`; it does **not** automatically import from Google Scholar. The Google Scholar link on the home page opens the live Scholar profile. When adding a paper, add its full citation, DOI or stable URL, and category to the JavaScript list; add an illustrated home-page summary only when there is a useful figure and the facts and reuse rights can be verified.

For a new research card, upload its image to `assets/work/`, add an `<article class="research-story">` inside `.research-stories` in `index.html`, and include a descriptive alt text, source/figure credit, license where applicable, concise summary, and publication link. Do not assume that an open-access paper allows reuse of every figure; check the figure or article license and any third-party credits.

To preview changes locally from this directory:

```sh
python3 -m http.server 4173
```

Then open <http://127.0.0.1:4173/>. To publish local edits, commit and push to `main`. GitHub documents the [branch publishing setup](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

The homepage URL is the stable destination for a QR code: `https://engflaviomartins.github.io/`. The HTML CV lives at `/cv/`; the PDF downloads remain optional.
