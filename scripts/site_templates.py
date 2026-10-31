"""Shared content, HTML components, and project templates for the portfolio."""
import html
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))
LINKEDIN = "https://www.linkedin.com/in/ramatridigdaya/"
GITHUB = "https://github.com/erzete"
SITE = "https://erzete.github.io"
HERO_INTRO = (
    "My name is Rama Tridigdaya. I build tools that make everyday work a little easier, especially when it involves "
    "repetitive tasks or systems that don’t quite talk to each other. These days, a lot of that work "
    "happens in Odoo. I also enjoy exploring new technology and finding out what it can do."
)


def esc(value):
    return html.escape(str(value), quote=True)


def head(title, description, slug=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{esc(description)}">
    <meta name="theme-color" content="#faf9f6">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:url" content="{SITE}/{slug}">
    <meta property="og:image" content="{SITE}/img/social-preview.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="{SITE}/{slug}">
    <link rel="icon" href="img/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="css/style.css">
    {('<link rel="stylesheet" href="css/projectstyle.css">' if slug else '')}
    <script>document.documentElement.classList.add('js');</script>
    <script src="js/site.js" defer></script>
    <title>{esc(title)}</title>
</head>
<body>
    <a class="skip-link" href="#main">Skip to content</a>'''


def nav(home=False):
    prefix = "" if home else "./"
    return f'''
    <header class="site-header">
        <nav class="nav wrap" aria-label="Main navigation">
            <a class="brand" href="./" aria-label="Rama Tridigdaya home"><span class="brand-mark" aria-hidden="true">RT</span><span class="brand-name">Rama Tridigdaya</span></a>
            <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-links">Menu <span class="menu-symbol" aria-hidden="true">+</span></button>
            <div class="nav-links" id="nav-links">
                <a href="{prefix}#projects">Work</a>
                <a href="{prefix}#about">About</a>
                <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a>
                <a class="nav-contact" href="{prefix}#contact">Let’s connect <span aria-hidden="true">↗</span></a>
            </div>
        </nav>
    </header>'''


def footer():
    return f'''
    <footer class="site-footer">
        <div class="footer-inner wrap">
            <p>© 2026 Rama Tridigdaya</p>
            <div class="footer-links"><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="#main">Back to top ↑</a></div>
        </div>
    </footer>
</body>
</html>
'''


def contact():
    return f'''
        <section class="contact wrap" id="contact" aria-labelledby="contact-title">
            <div><span class="eyebrow">Let’s connect</span><h2 id="contact-title">Good systems start<br>with a conversation.</h2><p>Have an interesting backend problem, an integration challenge, or just want to talk tech? Find me here.</p></div>
            <div class="actions"><a class="button button-primary" href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a><a class="button button-secondary" href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a></div>
        </section>'''


def tags(items):
    return '<ul class="tags" aria-label="Technologies">' + ''.join(f'<li>{esc(item)}</li>' for item in items) + '</ul>'


def png_dimensions(src):
    with (ROOT / src).open('rb') as file:
        data = file.read(24)
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Expected PNG: {src}')
    return struct.unpack('>II', data[16:24])


def image(src, alt):
    width, height = png_dimensions(src)
    return f'<img src="{esc(src)}" alt="{esc(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async">'


def mini_diagram(project):
    arrow = '↔' if project.get('bidirectional') else '→'
    nodes = []
    for index, text in enumerate(project['mini']):
        if index:
            nodes.append(f'<span class="mini-arrow">{arrow}</span>')
        nodes.append(f'<span class="mini-node{" center" if index == 1 else ""}">{esc(text)}</span>')
    return f'''<div class="card-visual tone-{project['tone']}" aria-hidden="true"><span class="diagram-label">{esc(project['category'])} / overview</span><div class="mini-flow">{''.join(nodes)}</div><span class="diagram-note">{esc(project['miniNote'])}</span></div>'''


def card(project, number, archive=False):
    classes = 'project-card' + (' archive-card' if archive else '') + (' wide' if archive and project['slug'] == 'scm' else '')
    visual = f'<div class="card-visual">{image(project["thumbnail"], project["thumbnailAlt"])}</div>' if 'thumbnail' in project else mini_diagram(project)
    status = f'<span class="card-status">{esc(project["status"])}</span>' if project.get('status') else ''
    return f'''
                <a class="{classes}" href="./{project['slug']}">
                    {visual}
                    <div class="card-content">
                        <div class="card-kicker"><span>{esc(project['category'])}</span><span>{number:02}</span></div>
                        <h3>{esc(project['title'])}</h3>
                        {status}
                        <p>{esc(project['summary'])}</p>
                        {tags(project['tech'])}
                        <span class="card-link">Explore project <span aria-hidden="true">↗</span></span>
                    </div>
                </a>'''


def legacy_homepage():
    selected = ''.join(card(project, i + 1) for i, project in enumerate(PROJECTS[:3]))
    more = ''.join(card(project, i + 4, archive=True) for i, project in enumerate(PROJECTS[3:]))
    return head('Rama Tridigdaya — Backend, ERP & Integrations', 'IT Engineer at Monotaro Indonesia. Explore Rama Tridigdaya’s work in backend systems, Odoo ERP, and integrations.') + nav(home=True) + f'''
    <main id="main">
        <section class="hero wrap" aria-labelledby="intro-title">
            <div>
                <span class="eyebrow">Backend / ERP / Integrations</span>
                <h1 id="intro-title">Making systems<br>work <em>together.</em></h1>
                <p class="hero-copy">{esc(HERO_INTRO)}</p>
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
        </section>

        <section class="section wrap" id="projects" aria-labelledby="work-title">
            <div class="section-heading"><div><span class="eyebrow">01 / Selected work</span><h2 id="work-title">Built around real workflows.</h2></div><p>A closer look at the systems I connect and the problems behind them.</p></div>
            <div class="featured-grid">{selected}
            </div>
        </section>

        <section class="section wrap" id="about" aria-labelledby="about-title">
            <div class="about-layout">
                <div class="about-copy"><span class="eyebrow">02 / Behind the work</span><h2 id="about-title">A backend engineer.<br>A curious problem solver.</h2><p>I’m an Information Systems graduate from Universitas Indonesia, now working on backend systems and ERP at Monotaro Indonesia.</p><p>My work spans Odoo, internal tools, and integrations between the platforms people use every day. I also like exploring new technology and figuring out where it can be useful.</p><p class="education"><strong>Universitas Indonesia</strong>Information Systems graduate</p></div>
                <div class="expertise" id="skills" aria-label="Skills and technologies">
                    <div class="expertise-group"><h3>Backend & ERP</h3><p>Python · Django · Spring Boot · Odoo · Oracle APEX</p></div>
                    <div class="expertise-group"><h3>Data & search</h3><p>PostgreSQL · MySQL<br>MongoDB · Meilisearch</p></div>
                    <div class="expertise-group"><h3>Integrations & AI</h3><p>Chatwoot · Zendesk<br>Meta API · AI Integration</p></div>
                    <div class="expertise-group"><h3>Frontend</h3><p>React · HTML · CSS</p></div>
                    <div class="expertise-group"><h3>Cloud & deployment</h3><p>GCP · Docker</p></div>
                </div>
            </div>
        </section>

        <section class="section wrap" aria-labelledby="more-title">
            <div class="section-heading"><div><span class="eyebrow">03 / More projects</span><h2 id="more-title">More things I’ve worked on.</h2></div><p>From warehouse operations to university projects in commerce, energy, and sports.</p></div>
            <div class="archive-grid">{more}
            </div>
        </section>
        {contact()}
    </main>''' + footer()


def flow(nodes, bidirectional=False):
    items = []
    for index, node in enumerate(nodes):
        items.append(f'''<li class="flow-node{' central' if index == 1 else ''}"><span class="flow-step">0{index + 1} / {esc(node['label'])}</span><strong>{esc(node['name'])}</strong><p>{esc(node['description'])}</p></li>''')
    direction = ' data-bidirectional' if bidirectional else ''
    flow_class = 'flow flow-long' if len(nodes) > 4 else 'flow'
    return f'<ol class="{flow_class}"{direction}>{"".join(items)}</ol>'


def diagram(project):
    if not project.get('showOverview', True):
        return ''
    return f'''
        <figure class="system-figure tone-{project['tone']}" aria-labelledby="diagram-title">
            <div class="figure-heading"><h2 id="diagram-title">{esc(project['flowTitle'])}</h2><span class="figure-index">System overview</span></div>
            {flow(project['nodes'], project.get('bidirectional', False))}
            <figcaption>{esc(project['flowNote'])}</figcaption>
        </figure>'''


def case_copy(project):
    if project.get('workflows'):
        return f'<section class="case-intro" aria-labelledby="context-title"><h2 id="context-title">The context</h2><p>{esc(project["context"])}</p></section>'
    features = ''.join(f'<li>{esc(feature)}</li>' for feature in project['features'])
    right = f'<section aria-labelledby="does-title"><h2 id="does-title">What it does</h2><ul class="feature-list">{features}</ul></section>'
    return f'<div class="case-copy"><section aria-labelledby="context-title"><h2 id="context-title">The context</h2><p>{esc(project["context"])}</p></section>{right}</div>'


def workflow_sections(project):
    if not project.get('workflows'):
        return ''
    items = []
    for index, item in enumerate(project['workflows']):
        compact_flow = ''
        if item.get('flow'):
            steps = ''.join(f'<li>{esc(step)}</li>' for step in item['flow'])
            compact_flow = f'<figure class="workflow-diagram" aria-label="{esc(item["title"])} flow"><ol class="workflow-flow">{steps}</ol></figure>'
        detail = f'<p class="workflow-detail">{esc(item["detail"])}</p>' if item.get('detail') else ''
        items.append(f'<li><span class="workflow-index" aria-hidden="true">{index + 1:02}</span><div class="workflow-content"><h3>{esc(item["title"])}</h3><p>{esc(item["body"])}</p>{compact_flow}{detail}</div></li>')
    eyebrow = project.get('workflowEyebrow', 'The procurement workflow')
    title = project.get('workflowTitle', 'What the integration automates.')
    return f'''<section class="workflow-section" aria-labelledby="workflows-title"><span class="eyebrow">{esc(eyebrow)}</span><h2 id="workflows-title">{esc(title)}</h2><ol class="workflow-list">{''.join(items)}</ol></section>'''


def decision_sections(project):
    if not project.get('decisions'):
        return ''
    items = ''.join(f'<article><h3>{esc(item["title"])}</h3><p>{esc(item["body"])}</p></article>' for item in project['decisions'])
    title = project.get('decisionsTitle', 'Designing around supplier behavior.')
    return f'''<section class="decision-section" aria-labelledby="decisions-title"><span class="eyebrow">Design decisions</span><h2 id="decisions-title">{esc(title)}</h2><div class="decision-grid">{items}</div></section>'''


def project_metrics(project):
    if not project.get('metrics'):
        return ''
    metrics = ''.join(f'<div><dt>{esc(item["label"])}</dt><dd>{esc(item["value"])}</dd></div>' for item in project['metrics'])
    return f'''<section class="project-results" aria-labelledby="results-title"><h2 class="eyebrow" id="results-title">{esc(project.get('metricsTitle', 'Operational scale'))}</h2><dl class="results-grid">{metrics}</dl><p class="results-note">{esc(project.get('metricsNote', ''))}</p></section>'''


def project_outcome(project):
    if not project.get('outcome'):
        return ''
    return f'<section class="project-outcome" aria-labelledby="outcome-title"><h2 class="eyebrow" id="outcome-title">Observed result</h2><p>{esc(project["outcome"])}</p></section>'


def gallery(project):
    if not project.get('gallery'):
        return ''
    slides = []
    for index, item in enumerate(project['gallery']):
        slides.append(f'''
                <figure class="gallery-slide" aria-label="Screenshot {index + 1} of {len(project['gallery'])}"><a href="{esc(item['src'])}" target="_blank" rel="noopener noreferrer" aria-label="Open full-size image: {esc(item['caption'])}">{image(item['src'], item['caption'])}</a><figcaption>{esc(item['caption'])}<span>Open image to view full size ↗</span></figcaption></figure>''')
    return f'''
        <section class="gallery-section" data-gallery aria-labelledby="gallery-title">
            <span class="eyebrow">Inside the application</span><h2 id="gallery-title">A look at the interface.</h2>
            <p class="gallery-intro">Swipe or scroll through the screenshots. Open an image for a closer look.</p>
            <div class="gallery-track" tabindex="0" role="region" aria-label="Project screenshots; use left and right arrow keys to navigate">{''.join(slides)}
            </div>
            <div class="gallery-controls" hidden><p aria-live="polite" aria-atomic="true">Screenshot <span data-count>1 / {len(project['gallery'])}</span></p><div class="gallery-buttons"><button type="button" data-previous aria-label="Previous screenshot">←</button><button type="button" data-next aria-label="Next screenshot">→</button></div></div>
        </section>'''


def project_page(project, next_project):
    narrative = case_copy(project)
    started = f'<div><span class="meta-label">Started</span><p>{esc(project["started"])}</p></div>' if project.get('started') else ''
    meta_class = 'project-meta with-timeline' if started else 'project-meta'
    status = f'<p class="project-status">{esc(project["status"])}</p>' if project.get('status') else ''
    return head(f"{project['title']} — Rama Tridigdaya", project['summary'], project['slug']) + nav() + f'''
    <main id="main" class="wrap">
        <header class="project-header">
            <nav class="breadcrumb" aria-label="Breadcrumb"><a href="./#projects">Work</a><span aria-hidden="true">/</span><span aria-current="page">{esc(project['title'])}</span></nav>
            <span class="eyebrow">{esc(project['kind'])} / {esc(project['category'])}</span>
            {status}
            <h1>{esc(project['title'])}</h1>
            <p class="project-summary">{esc(project['summary'])}</p>
            <div class="{meta_class}"><div><span class="meta-label">Focus</span><p>{esc(project['focus'])}</p></div>{started}<div><span class="meta-label">Built with</span>{tags(project['tech'])}</div></div>
        </header>
        {project_metrics(project)}
        {narrative if project.get('workflows') else ''}
        {diagram(project)}
        {'' if project.get('workflows') else narrative}
        {workflow_sections(project)}
        {project_outcome(project)}
        {decision_sections(project)}
        {gallery(project)}
        <nav class="next-project" aria-label="Project navigation"><a href="./{next_project['slug']}"><span class="eyebrow">Next project</span><span class="next-title">{esc(next_project['title'])}</span></a><span class="next-arrow" aria-hidden="true">↗</span></nav>
    </main>
    {contact()}''' + footer()
