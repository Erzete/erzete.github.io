"""Generate the default portfolio HTML. GitHub Pages needs no build step.

Run python scripts/build.py after editing project content or templates.
"""
from build_directions import homepage, project_page
from site_templates import ROOT, PROJECTS


def write_page(path, markup):
    path.write_text('\n'.join(line.rstrip() for line in markup.splitlines()) + '\n', encoding='utf-8')


def main():
    write_page(ROOT / 'index.html', homepage('bold-grid', preview=False))
    for index, project in enumerate(PROJECTS):
        next_project = PROJECTS[(index + 1) % len(PROJECTS)]
        write_page(ROOT / f"{project['slug']}.html", project_page(project, next_project, 'bold-grid', preview=False))
    print(f'Generated default homepage and {len(PROJECTS)} project pages.')


if __name__ == '__main__':
    main()
