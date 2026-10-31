# Rama Tridigdaya — portfolio

A static personal portfolio served directly by GitHub Pages. No package installation,
framework, or server-side code is needed for hosting. HTML, CSS, JavaScript, and assets
are committed to this repository.

## Preview locally

```sh
python scripts/preview.py
```

Open <http://127.0.0.1:4173>. The preview supports the same extensionless project links
used on the live site. Stop with Ctrl+C.

## Compare full-site design directions

```sh
python scripts/build_directions.py
python scripts/check.py --previews
python scripts/preview.py
```

Open `/previews/work-first/` or `/previews/bold-grid/` on the local preview server.
Each direction includes the homepage and all eight project pages. The comparison
bar switches to the same page in the other direction. Previews use the same project
content and assets as the main site, with `css/directions.css` defining their styles.
Generated `/previews/` files are ignored by Git. Bold is the default design at the
site root, without the comparison bar.

## Edit project content

Project descriptions, technologies, diagrams, and screenshot order live in
`content/projects.json`. After editing, regenerate the committed HTML:

```sh
python scripts/build.py
python scripts/check.py
```

The optional generator uses only the Python standard library. GitHub Pages serves
the generated files as they are; it does not need to run Python. Homepage layouts
are in `scripts/build_directions.py`; intro copy and shared project templates are
in `scripts/site_templates.py`. `scripts/build.py` generates the chosen default.
Generated HTML files should be
updated through that source so a later regeneration preserves the changes.

## Design and behavior

- `css/style.css`: shared light theme, navigation, homepage, and footer.
- `css/projectstyle.css`: case-study diagrams and screenshot galleries.
- `css/directions.css`: default Bold layout and optional Work first preview styles.
- `js/site.js`: mobile navigation and manual, keyboard-accessible galleries.
- `img/thumbs/`: small homepage previews; original screenshots remain untouched.
- `img/social-preview.png`: social-sharing preview.

On Windows, `scripts/prepare-images.ps1` optionally regenerates the four thumbnails
and social preview using built-in System.Drawing. Run it before `scripts/build.py`
if thumbnail sources change. No external fonts or icon CDNs are required.

Diagrams currently show conceptual system or workflow overviews. They deliberately
avoid asserting deployment architecture, ownership, or measured outcomes until those
details are confirmed in the project interviews.
