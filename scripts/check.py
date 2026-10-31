"""Check generated HTML, local links, fragments, and image accessibility."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import argparse

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.links = []
        self.errors = []
        self.headings = 0
        self.description = False
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.errors.append(f'Duplicate ID: {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.headings += 1
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = bool(attrs.get('content'))
        if tag == 'img':
            for attribute in ('alt', 'width', 'height'):
                if not attrs.get(attribute):
                    self.errors.append(f'Image missing {attribute}: {attrs.get("src")}')
        for key in ('src', 'href'):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previews', action='store_true', help='Also check both full-site design previews')
    args = parser.parse_args()
    paths = list(ROOT.glob('*.html'))
    if args.previews:
        paths.extend((ROOT / 'previews').rglob('*.html'))
    pages = {path.resolve(): Page(path) for path in paths}
    errors = []
    count = 0
    for path, page in pages.items():
        if page.headings != 1:
            page.errors.append(f'Expected one H1, found {page.headings}')
        if not page.description:
            page.errors.append('Missing description')
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if target.is_dir():
                target /= 'index.html'
            elif not target.exists() and not target.suffix:
                target = target.with_suffix('.html')
            count += 1
            if not target.is_file():
                page.errors.append(f'Missing local target: {link}')
            elif parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
                page.errors.append(f'Missing anchor: {link}')
        errors.extend(f'{path.name}: {error}' for error in page.errors)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'Passed: {len(pages)} pages, {count} local references, image attributes, descriptions, and heading structure.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
