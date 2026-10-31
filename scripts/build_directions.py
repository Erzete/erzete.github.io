"""Default Bold layout and optional, complete local design previews.

Run python scripts/build_directions.py, then python scripts/preview.py.
The current site is untouched. Generated previews are ignored by Git.
"""
from pathlib import Path
import site_templates as site

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'previews'
DIRECTIONS = {'work-first': 'Work first', 'bold-grid': 'Bold grid'}
BY_SLUG = {project['slug']: project for project in site.PROJECTS}
INTRO = 'Backend engineering across ERP, product search, and internal tools.'
BOLD_INTRO = site.HERO_INTRO


def page_shell(markup, direction, slug='', preview=True):
    markup = markup.replace('<body>', f'<body class="direction-{direction}">')
    if preview:
        other = 'bold-grid' if direction == 'work-first' else 'work-first'
        destination = slug or './'
        bar = f'''<aside class="direction-bar" aria-label="Design comparison"><div class="wrap"><span>Design preview / <strong>{DIRECTIONS[direction]}</strong></span><a href="../{other}/{destination}">View {DIRECTIONS[other]} <span aria-hidden="true">↗</span></a></div></aside>'''
        markup = markup.replace('<header class="site-header">', bar + '<header class="site-header">', 1)
        # Asset paths point to shared files; page navigation stays inside each design.
        for attribute, folder in [('href', 'css/'), ('href', 'img/'), ('src', 'img/'), ('src', 'js/')]:
            markup = markup.replace(f'{attribute}="{folder}', f'{attribute}="../../{folder}')
        extra_head = '<meta name="robots" content="noindex">\n<link rel="stylesheet" href="../../css/directions.css">'
    else:
        extra_head = '<link rel="stylesheet" href="css/directions.css">'
    markup = markup.replace('</head>', extra_head + '\n</head>')
    return markup


def project_label(project):
    if project['slug'] == 'odoo-whatsapp':
        return '>50%', 'outbound messages automated'
    if project['slug'] == 'meilisearch':
        return '6M', 'SKUs indexed'
    if project['slug'] == 'chatdesk':
        return 'Zendesk', 'custom sidebar app'
    return 'Oracle APEX', 'awaiting operational use'


def ledger_row(project, number, archive=False):
    status = f'<span class="card-status">{site.esc(project["status"])}</span>' if project.get('status') else ''
    if archive and project.get('thumbnail'):
        leading = f'<div class="ledger-image">{site.image(project["thumbnail"], project["thumbnailAlt"])}</div>'
    else:
        leading = f'<span class="ledger-number">{number:02}</span>'
    scale = ''
    if not archive:
        value, label = project_label(project)
        scale = f'<div class="ledger-scale"><strong>{value}</strong><span>{label}</span></div>'
    return f'''<a class="ledger-row{' ledger-archive' if archive else ''}" href="./{project['slug']}">{leading}<div class="ledger-copy"><span class="eyebrow">{site.esc(project['category'])}</span><h3>{site.esc(project['title'])}</h3>{status}<p>{site.esc(project['summary'])}</p><span class="ledger-tech">{' / '.join(site.esc(item) for item in project['tech'][:4])}</span></div>{scale}<span class="ledger-arrow" aria-hidden="true">↗</span></a>'''


def about():
    return '''<section class="section wrap direction-about" id="about" aria-labelledby="about-title"><div class="about-layout"><div class="about-copy"><span class="eyebrow">About</span><h2 id="about-title">Behind the work.</h2><p>I’m Rama Tridigdaya, an Information Systems graduate from Universitas Indonesia and an IT Engineer at Monotaro Indonesia.</p><p>My work covers Odoo procurement workflows, backend integrations, product search, and internal tools for the people running day-to-day operations.</p><p class="education"><strong>Universitas Indonesia</strong>Information Systems graduate</p></div><div class="expertise" aria-label="Skills and technologies"><div class="expertise-group"><h3>Backend & ERP</h3><p>Python / Django / Spring Boot<br>Odoo / Oracle APEX</p></div><div class="expertise-group"><h3>Data & search</h3><p>SQL / PostgreSQL / MySQL<br>BigQuery / Meilisearch</p></div><div class="expertise-group"><h3>Integrations</h3><p>Chatwoot / Zendesk<br>Meta WhatsApp API</p></div><div class="expertise-group"><h3>Cloud & interfaces</h3><p>GCP / Docker<br>React / HTML / CSS</p></div></div></div></section>'''


def contact():
    return f'''<section class="contact wrap" id="contact" aria-labelledby="contact-title"><div><span class="eyebrow">Get in touch</span><h2 id="contact-title">Let’s connect.</h2><p>Find me on LinkedIn or explore more of my work on GitHub.</p></div><div class="actions"><a class="button button-primary" href="{site.LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a class="button button-secondary" href="{site.GITHUB}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></section>'''


def archive(direction):
    if direction == 'work-first':
        items = ''.join(ledger_row(project, i + 4, True) for i, project in enumerate(site.PROJECTS[3:]))
        layout = 'project-ledger archive-ledger'
    else:
        items = ''.join(site.card(project, i + 4, archive=True) for i, project in enumerate(site.PROJECTS[3:]))
        layout = 'archive-grid'
    return f'''<section class="section wrap" aria-labelledby="more-title"><div class="section-heading"><div><span class="eyebrow">More projects</span><h2 id="more-title">Further work.</h2></div><p>Warehouse operations and university projects in commerce, energy, and sports.</p></div><div class="{layout}">{items}</div></section>'''


def bold_feature(project):
    featured = project['slug'] == 'odoo-whatsapp'
    scale = ''
    if featured:
        metric = project['metrics'][0]
        scale = f'<div class="mosaic-scale">{site.esc(metric["value"])}<span>{site.esc(metric["label"])}</span></div>'
    return f'''<a class="mosaic-project{' mosaic-featured' if featured else ''}" href="./{project['slug']}"><span class="eyebrow">{site.esc(project['category'])}</span><h3>{site.esc(project['title'])}</h3><p>{site.esc(project['summary'])}</p>{scale}<span class="mosaic-bottom"><span>{' / '.join(site.esc(item) for item in project['tech'][:3])}</span><span aria-hidden="true">↗</span></span></a>'''


def bold_opening():
    return f'''<section class="hero wrap" aria-labelledby="intro-title">
        <div>
            <span class="eyebrow">Backend / ERP / Integrations</span>
            <h1 id="intro-title">Making systems<br>work <em>together.</em></h1>
            <p class="hero-copy">{site.esc(BOLD_INTRO)}</p>
            <p class="hero-role"><strong>IT Engineer</strong> at Monotaro Indonesia</p>
            <div class="actions"><a class="button button-primary" href="#projects">Explore my work <span aria-hidden="true">↓</span></a><a class="button button-secondary" href="#about">A little about me <span aria-hidden="true">↗</span></a></div>
        </div>
        <div class="hero-visual" aria-label="My work connects people and processes, backend and ERP systems, and the tools teams use.">
            <div class="visual-top" aria-hidden="true"><span>The work, at a glance</span><span>RT / 01</span></div>
            <div class="hero-map" aria-hidden="true">
                <div class="map-node"><span class="node-number">01</span><div><strong>People & processes</strong><small>Procurement · Support · Operations</small></div></div>
                <div class="map-connector">understand the workflow</div>
                <div class="map-node central"><span class="node-number">02</span><div><strong>Backend & ERP</strong><small>Python · Odoo · APIs</small></div></div>
                <div class="map-connector">connect the right systems</div>
                <div class="map-node"><span class="node-number">03</span><div><strong>The tools teams use</strong><small>WhatsApp · Zendesk · Search</small></div></div>
            </div>
            <div class="visual-bottom" aria-hidden="true"><span>Less switching. More doing.</span><span>↗</span></div>
        </div>
    </section>'''


def homepage(direction, preview=True):
    if direction == 'work-first':
        hero = f'''<section class="direction-hero wrap" aria-labelledby="intro-title"><div><span class="eyebrow">Selected work / Portfolio</span><h1 id="intro-title">Rama<br>Tridigdaya.</h1></div><div class="hero-description"><h2>Backend & ERP<br>engineering.</h2><p>{INTRO}</p><p class="hero-position"><strong>IT Engineer</strong><br>Monotaro Indonesia</p></div></section>'''
        projects = ''.join(ledger_row(BY_SLUG[slug], i + 1) for i, slug in enumerate(['odoo-whatsapp', 'meilisearch', 'chatdesk']))
        work = f'''<section class="section wrap selected-section" id="projects" aria-labelledby="work-title"><div class="section-heading"><h2 id="work-title">Selected work</h2><span class="eyebrow">Backend / Integrations / Search</span></div><div class="project-ledger">{projects}</div></section>'''
    else:
        hero = bold_opening()
        projects = ''.join(bold_feature(BY_SLUG[slug]) for slug in ['odoo-whatsapp', 'meilisearch', 'chatdesk'])
        work = f'''<section class="section wrap selected-section" id="projects" aria-labelledby="work-title"><div class="section-heading"><h2 id="work-title">Selected work</h2><span class="eyebrow">Procurement / Search / Support</span></div><div class="mosaic-grid">{projects}</div></section>'''
    description = BOLD_INTRO if direction == 'bold-grid' else INTRO
    markup = site.head('Rama Tridigdaya — Backend, ERP & Integrations', description) + site.nav(home=True) + '<main id="main">' + hero + work + about() + archive(direction) + contact() + '</main>' + site.footer()
    return page_shell(markup, direction, preview=preview)


def project_page(project, next_project, direction, preview=True):
    # Reuse the factual narrative, compact flows, and original screenshot galleries.
    markup = site.project_page(project, next_project)
    markup = markup.replace(site.contact(), contact())
    markup = markup.replace('<main id="main" class="wrap">', '<main id="main" class="wrap case-study">')
    return page_shell(markup, direction, project['slug'], preview=preview)


def main():
    for direction in DIRECTIONS:
        folder = OUTPUT / direction
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(homepage(direction), encoding='utf-8')
        for index, project in enumerate(site.PROJECTS):
            next_project = site.PROJECTS[(index + 1) % len(site.PROJECTS)]
            (folder / f'{project["slug"]}.html').write_text(project_page(project, next_project, direction), encoding='utf-8')
    print('Generated 18 pages: http://127.0.0.1:4173/previews/work-first/')
    print('Compare: http://127.0.0.1:4173/previews/bold-grid/')


if __name__ == '__main__':
    main()
