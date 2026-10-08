#!/usr/bin/env python3
"""Publish the verified PStack corpus as an offline-built learning site."""
import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from typing import Optional

import bleach
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt
from markupsafe import Markup

import bilingual

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'KonsonChow/pstack'
SECTIONS = {
    'guide': ('学习指南', '按十个章节，从安装走到独立使用。'),
    'skills': ('技能手册', '按任务找到技能，了解触发条件与执行步骤。'),
    'principles': ('工作原则', '用原则名字指出问题，改变代理下一步的选择。'),
    'playbooks': ('执行规程', '从调查、实现到交付，每类任务都有自己的步骤。'),
    'agents': ('代理角色', '了解执行代理与独立审阅者的职责。'),
    'automations': ('自动化', '学习 Benny 如何接收问题、分流与复现。'),
    'references': ('参考材料', '提示词、检查清单和模板，按所属技能查阅。'),
    'about': ('关于项目', '项目全貌、来源与镜像同步方式。'),
}
MD = MarkdownIt('commonmark', {'html': True}).enable('table').enable('strikethrough')
SAFE_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code', 'hr', 'br',
    'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'details', 'summary', 'del',
}


@dataclass(frozen=True)
class Document:
    source: PurePosixPath
    route: str
    section: str
    parent: Optional[PurePosixPath]
    title_en: str
    title_zh: str
    blocks: tuple[dict[str, str], ...]

    def markdown(self, language):
        text = ''.join(block['en'] for block in self.blocks) if language == 'en' else '\n\n'.join(block['zh'].rstrip() for block in self.blocks) + '\n'
        return re.sub(r'\A---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.S)


@dataclass(frozen=True)
class Catalog:
    by_source: dict[PurePosixPath, Document]
    by_route: dict[str, Document]

    def section(self, name):
        return [doc for doc in self.by_source.values() if doc.section == name]


def route_for(source):
    parts = source.parts
    if parts[:2] == ('docs', 'guide'):
        return ('/guide/' if source.name == 'README.md' else '/guide/' + source.stem + '/'), 'guide'
    if parts[:3] == ('skills', 'poteto-mode', 'playbooks'):
        return '/playbooks/' + source.stem + '/', 'playbooks'
    if parts[0] == 'skills' and source.name == 'SKILL.md':
        name = parts[1]
        return ('/principles/' + name[len('principle-'):] + '/', 'principles') if name.startswith('principle-') else ('/skills/' + name + '/', 'skills')
    if parts[0] == 'skills':
        return '/' + str(source.with_suffix('')).removesuffix('/README') + '/', 'references'
    if parts[0] in ('agents', 'automations'):
        return '/' + str(source.with_suffix('')).removesuffix('/README').removesuffix('/SKILL') + '/', parts[0]
    if len(parts) == 1:
        return '/about/' + ('pstack' if source.name == 'README.md' else source.stem.lower()) + '/', 'about'
    return '/references/' + str(source.with_suffix('')) + '/', 'references'


def title_of(markdown, fallback):
    tokens = MD.parse(re.sub(r'\A---\s*\n.*?\n---\s*\n', '', markdown, count=1, flags=re.S))
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            return tokens[i + 1].content.replace('`', '')
    return fallback


def load_catalog(root=ROOT):
    documents = []
    for path in bilingual.sources():
        source = PurePosixPath(path.relative_to(root).as_posix())
        data_path = root / 'translations/zh-CN' / (str(source) + '.json')
        if not data_path.is_file():
            raise ValueError(f'{source}: translation missing')
        data = json.loads(data_path.read_text())
        original = path.read_text()
        if data['source'] != str(source) or data['sha256'] != hashlib.sha256(original.encode()).hexdigest():
            raise ValueError(f'{source}: stale translation; review before publishing')
        if ''.join(block['en'] for block in data['blocks']) != original:
            raise ValueError(f'{source}: English differs from source')
        if any(not isinstance(block.get('zh'), str) or not block['zh'].strip() for block in data['blocks']):
            raise ValueError(f'{source}: untranslated block')
        route, section = route_for(source)
        parent = None
        for directory in source.parents:
            candidates = [directory / 'SKILL.md', directory / 'README.md']
            parent = next((candidate for candidate in candidates if candidate != source and (root / candidate).is_file()), None)
            if parent:
                break
        blocks = tuple(data['blocks'])
        documents.append(Document(source, route, section, parent, title_of(original, source.stem), title_of('\n\n'.join(b['zh'].rstrip() for b in blocks), source.stem), blocks))
    by_source = {doc.source: doc for doc in documents}
    by_route = {doc.route: doc for doc in documents}
    if len(by_route) != len(documents):
        raise ValueError('Duplicate document routes')
    return Catalog(by_source, by_route)


def slug(text):
    text = re.sub(r'<[^>]*>', '', text).lower()
    return ''.join(c for c in text if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')


def heading_data(tokens):
    used = set()
    result = []
    for i, token in enumerate(tokens):
        if token.type != 'heading_open':
            continue
        inline = tokens[i + 1]
        text = ''.join(child.content for child in inline.children or [] if child.type in ('text', 'code_inline', 'html_inline'))
        stem = slug(text)
        anchor = stem
        suffix = 0
        while anchor in used:
            suffix += 1
            anchor = f'{stem}-{suffix}'
        used.add(anchor)
        result.append((token, anchor, inline.content, int(token.tag[1])))
    return result


def base_path(value):
    if not value.startswith('/') or '?' in value or '#' in value or '..' in value:
        raise ValueError('Base must be an absolute URL path such as /pstack/ or /')
    return '/' + value.strip('/') + '/' if value.strip('/') else '/'


def site_url(base, route):
    return base + route.lstrip('/')


def rewrite_link(catalog, doc, href, base, revision, root, output, defects):
    url = urlsplit(href)
    if url.scheme or url.netloc:
        return href
    if not url.path:
        return href
    path = PurePosixPath(posixpath.normpath(posixpath.join(str(doc.source.parent), unquote(url.path))))
    if url.path.startswith('/'):
        path = PurePosixPath(unquote(url.path).lstrip('/'))
    target = catalog.by_source.get(path)
    if not target:
        target = catalog.by_source.get(path / 'README.md') or catalog.by_source.get(path / 'SKILL.md')
    if target:
        return urlunsplit(('', '', site_url(base, target.route), url.query, url.fragment))
    local = root / path
    if local.is_dir():
        collection = '/' + str(path).strip('/') + '/'
        if collection.strip('/') in SECTIONS:
            return urlunsplit(('', '', site_url(base, collection), url.query, url.fragment))
        return f'https://github.com/{REPOSITORY}/tree/{revision}/{quote(str(path))}'
    if local.is_file() and local.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'):
        dest = output / 'assets/source' / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(local, dest)
        return urlunsplit(('', '', site_url(base, '/assets/source/' + str(path)), url.query, url.fragment))
    if not local.exists():
        defect = {'source': str(doc.source), 'target': href, 'reason': 'missing source target'}
        if defect not in defects:
            defects.append(defect)
    return f'https://github.com/{REPOSITORY}/blob/{revision}/{quote(str(path))}' + (('#' + url.fragment) if url.fragment else '')


def render_document(catalog, doc, base, revision, root, output, defects):
    parsed = {lang: MD.parse(doc.markdown(lang)) for lang in ('en', 'zh')}
    headings = {lang: heading_data(tokens) for lang, tokens in parsed.items()}
    if len(headings['en']) != len(headings['zh']):
        raise ValueError(f'{doc.source}: translated heading count differs')
    toc = []
    rendered = {}
    for lang, tokens in parsed.items():
        for index, (token, own_anchor, label, level) in enumerate(headings[lang]):
            anchor = headings['en'][index][1]
            token.attrSet('id', ('' if lang == 'zh' else 'en-') + anchor)
            token.attrSet('data-anchor', anchor)
            if index == 0:
                token.attrSet('data-document-title', 'true')
            if lang == 'zh' and index > 0 and level in (2, 3):
                toc.append({'anchor': anchor, 'title': label.replace('`', ''), 'level': level})
        for token in tokens:
            for child in token.children or []:
                attribute = 'href' if child.type == 'link_open' else 'src' if child.type == 'image' else None
                if attribute:
                    href = child.attrGet(attribute)
                    child.attrSet(attribute, rewrite_link(catalog, doc, href, base, revision, root, output, defects))
        html = MD.renderer.render(tokens, MD.options, {})
        rendered[lang] = Markup(bleach.clean(html, tags=SAFE_TAGS, attributes={'*': ['id', 'data-anchor', 'data-document-title'], 'a': ['href', 'title'], 'img': ['src', 'alt', 'title'], 'code': ['class'], 'details': ['open'], 'th': ['align'], 'td': ['align']}, protocols=['http', 'https', 'mailto'], strip=False))
    return rendered, toc


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def verify_site(output):
    manifest = json.loads((output / 'manifest.json').read_text())
    base = manifest['base']
    pages = {}
    errors = []
    for path in output.rglob('*.html'):
        page = PageLinks()
        page.feed(path.read_text())
        if len(page.ids) != len(set(page.ids)):
            errors.append(f'{path.relative_to(output)}: duplicate HTML ids')
        pages[path] = page
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            if not url.path:
                target = path
            elif url.path.startswith(base):
                target = output / unquote(url.path[len(base):])
            else:
                errors.append(f'{path.relative_to(output)}: URL escapes base {href}')
                continue
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{path.relative_to(output)}: missing {href}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(output)}: missing anchor {href}')
    for doc in manifest['documents']:
        if not (output / doc['route'].lstrip('/') / 'index.html').is_file():
            errors.append(f'Missing route for {doc["source"]}')
    if errors:
        raise ValueError('\n'.join(sorted(set(errors))))
    print(f'Verified {len(manifest["documents"])} document routes and {len(pages)} HTML pages at {base}.')


def _build_site(output, base, root=ROOT):
    catalog = load_catalog(root)
    output.mkdir(parents=True, exist_ok=True)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    version = json.loads((root / '.cursor-plugin/plugin.json').read_text())['version']
    snapshot = json.loads((root / 'website/upstream.json').read_text())
    provenance = content_provenance(root)
    for feed in snapshot['feeds']:
        feed['imported'] = provenance['original' if feed['path'] else 'mirror']
        feed['compare_url'] = f'https://github.com/{feed["repository"]}/compare/{feed["imported"]}...{feed["head"]}'
    env = Environment(loader=FileSystemLoader(root / 'website/templates'), autoescape=select_autoescape(['html']))
    env.globals['url'] = lambda route: site_url(base, route)
    env.globals['sections'] = SECTIONS
    env.globals['catalog'] = catalog
    env.globals['published'] = {'revision': revision, 'version': version, 'count': len(catalog.by_source), 'upstream_base': provenance['mirror'], 'original_base': provenance['original']}
    env.globals['snapshot'] = snapshot
    env.globals['repository'] = REPOSITORY
    env.globals['base'] = base
    shutil.copytree(root / 'website/assets', output / 'assets', dirs_exist_ok=True)
    defects, search = [], []
    def write(route, template, **values):
        dest = output / route.lstrip('/') / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(env.get_template(template).render(route=route, **values))
    guides = sorted([doc for doc in catalog.section('guide') if doc.route != '/guide/'], key=lambda doc: doc.route)
    for doc in catalog.by_source.values():
        content, toc = render_document(catalog, doc, base, revision, root, output, defects)
        index = guides.index(doc) if doc in guides else -1
        previous = guides[index - 1] if index > 0 else None
        following = guides[index + 1] if 0 <= index < len(guides) - 1 else None
        write(doc.route, 'article.html', title=doc.title_zh, doc=doc, content=content, toc=toc, previous=previous, following=following, owner=catalog.by_source.get(doc.parent), children=[child for child in catalog.by_source.values() if child.parent == doc.source])
        search.append({'title': doc.title_zh, 'english': doc.title_en, 'section': SECTIONS[doc.section][0], 'url': site_url(base, doc.route), 'text': re.sub(r'\s+', ' ', doc.markdown('zh') + '\n' + doc.markdown('en'))})
    for section, (title, description) in SECTIONS.items():
        if '/' + section + '/' not in catalog.by_route:
            write('/' + section + '/', 'collection.html', title=title, description=description, documents=catalog.section(section), section=section, groups=principle_groups(catalog) if section == 'principles' else [('', catalog.section(section))])
    for filename, route in [('GLOSSARY.md', '/reference/glossary/'), ('SOURCE_NOTES.md', '/reference/source-notes/')]:
        original = (root / 'docs/bilingual' / filename).read_text()
        editorial = Document(PurePosixPath(filename), route, 'references', None, '', '', ({'en': original, 'zh': original},))
        content, _ = render_document(catalog, editorial, base, revision, root, output, defects)
        write(route, 'editorial.html', title=title_of(original, filename), content=content['zh'])
        search.append({'title': title_of(original, filename), 'english': filename, 'section': '本站编者注', 'url': site_url(base, route), 'text': original})
    write('/', 'home.html', title='PStack 中文学习站', guides=guides)
    write('/changes/', 'changes.html', title='上游变更', defects=defects)
    write('/search/', 'search.html', title='搜索完整文库')
    write('/library/', 'library.html', title='完整文库')
    manifest = {'generator': 'pstack-learning-pages', 'base': base, 'published': env.globals['published'], 'documents': [{'source': str(doc.source), 'route': doc.route, 'section': doc.section, 'parent': str(doc.parent) if doc.parent else None} for doc in catalog.by_source.values()], 'source_defects': defects}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (output / 'search.json').write_text(json.dumps(search, ensure_ascii=False) + '\n')
    (output / '.nojekyll').touch()
    (output / '404.html').write_text(env.get_template('not-found.html').render(title='页面未找到', route='/404/'))
    print(f'Built {len(catalog.by_source)} translated documents and 2 editorial pages. Source link defects: {len(defects)}. See manifest.json.')
    verify_site(output)


def content_provenance(root):
    data = json.loads((root / 'website/content-provenance.json').read_text())
    for field in ('mirror', 'original'):
        if not re.fullmatch(r'[a-f0-9]{7,40}', data[field]):
            raise ValueError(f'Invalid provenance revision {field}')
    subprocess.run(['git', 'merge-base', '--is-ancestor', data['mirror'], 'HEAD'], cwd=root, check=True)
    version = json.loads((root / '.cursor-plugin/plugin.json').read_text())['version']
    if data['version'] != version:
        raise ValueError('Update website/content-provenance.json after reviewing the source import')
    return data


def principle_groups(catalog):
    titles = {'Core': '核心原则', 'Architecture': '架构', 'Verification': '验证', 'Delegation': '委派', 'Meta': '改进工作方式'}
    groups = []
    source = catalog.by_source[PurePosixPath('skills/poteto-mode/SKILL.md')].markdown('en')
    section = source.split('## Principles', 1)[1].split('\n## ', 1)[0]
    for part in re.split(r'(?m)^\*\*(Core|Architecture|Verification|Delegation|Meta)\*\*\s*$', section)[1:]:
        if part in titles:
            groups.append((titles[part], []))
        elif groups:
            for name in re.findall(r'\*\*(principle-[a-z-]+)\*\*', part):
                doc = catalog.by_source.get(PurePosixPath('skills') / name / 'SKILL.md')
                if doc:
                    groups[-1][1].append(doc)
    grouped = {doc.source for _, docs in groups for doc in docs}
    remainder = [doc for doc in catalog.section('principles') if doc.source not in grouped]
    if remainder:
        groups.append(('其他原则', remainder))
    return groups


def build_site(output, base, root=ROOT):
    if output.exists() and any(output.iterdir()):
        manifest = output / 'manifest.json'
        if not manifest.is_file() or json.loads(manifest.read_text()).get('generator') != 'pstack-learning-pages':
            raise ValueError('Refusing to replace an output directory not owned by this generator')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pstack-site-', dir=output.parent) as directory:
        staged = Path(directory) / 'site'
        _build_site(staged, base, root)
        if output.exists():
            shutil.rmtree(output)
        staged.rename(output)


def refresh_upstream(root=ROOT):
    provenance = content_provenance(root)
    feeds = []
    checked = datetime.now(timezone.utc).isoformat(timespec='seconds')
    for repository, label, path, imported in (
        ('backnotprop/pstack', '独立仓库', None, provenance['mirror']),
        ('cursor/plugins', 'Cursor 原始上游', 'pstack', provenance['original']),
    ):
        query = {'sha': 'main', 'per_page': 30}
        if path:
            query['path'] = path
        endpoint = f'https://api.github.com/repos/{repository}/commits?' + urlencode(query)
        headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'pstack-learning-pages'}
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
        with urlopen(Request(endpoint, headers=headers), timeout=30) as response:
            commits = json.load(response)
        if not isinstance(commits, list) or not commits:
            raise ValueError(f'No commit history returned for {repository}')
        feeds.append({'repository': repository, 'label': label, 'path': path, 'checked_at': checked, 'head': commits[0]['sha'], 'imported': imported, 'api_url': endpoint, 'history_url': f'https://github.com/{repository}/commits/main' + ('/pstack' if path else ''), 'compare_url': f'https://github.com/{repository}/compare/{imported}...{commits[0]["sha"]}', 'commits': [{'sha': item['sha'], 'date': item['commit']['committer']['date'], 'subject': item['commit']['message'].splitlines()[0], 'url': item['html_url']} for item in commits]})
    dest = root / 'website/upstream.json'
    temporary = dest.with_suffix('.tmp')
    temporary.write_text(json.dumps({'feeds': feeds}, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(dest)
    print(f'Refreshed both upstream feeds at {checked}. Source and translations unchanged.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check', 'refresh-upstream'])
    parser.add_argument('--output', type=Path, default=ROOT / '.translation-work/site')
    parser.add_argument('--base', default='/pstack/')
    args = parser.parse_args()
    try:
        if args.command == 'refresh-upstream':
            refresh_upstream()
        elif args.command == 'check':
            verify_site(args.output.resolve())
        else:
            build_site(args.output.resolve(), base_path(args.base))
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
