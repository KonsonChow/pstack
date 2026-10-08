import importlib.util
import json
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('pstack_site', Path(__file__).with_name('site.py'))
site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(site)


class PublishingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = site.load_catalog()
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name) / 'public'
        site.build_site(cls.output, '/pstack/')

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_complete_corpus_and_semantic_routes(self):
        manifest = json.loads((self.output / 'manifest.json').read_text())
        self.assertEqual({entry['source'] for entry in manifest['documents']}, {str(path.relative_to(site.ROOT)) for path in site.bilingual.sources()})
        expected = {
            'docs/guide/01-setup.md': '/guide/01-setup/',
            'skills/architect/SKILL.md': '/skills/architect/',
            'skills/principle-model-the-domain/SKILL.md': '/principles/model-the-domain/',
            'skills/poteto-mode/playbooks/feature.md': '/playbooks/feature/',
            'skills/architect/references/rationale-template.md': '/skills/architect/references/rationale-template/',
            'automations/benny/README.md': '/automations/benny/',
        }
        actual = {item['source']: item['route'] for item in manifest['documents']}
        for source, route in expected.items():
            self.assertEqual(actual[source], route)
            self.assertTrue((self.output / route.lstrip('/') / 'index.html').is_file())
        self.assertEqual(manifest['source_defects'], [{'source': 'skills/why/references/synthesizer-prompt.md', 'target': 'url', 'reason': 'missing source target'}])

    def test_heading_suffixes_are_unique(self):
        tokens = site.MD.parse('# A\n\n## A\n\n## A-1\n\n## A\n')
        self.assertEqual([item[1] for item in site.heading_data(tokens)], ['a', 'a-1', 'a-1-1', 'a-2'])

    def test_chinese_paragraphs_preserve_headings(self):
        doc = self.catalog.by_source[PurePosixPath('MIRROR.md')]
        headings = site.heading_data(site.MD.parse(doc.markdown('zh')))
        self.assertEqual([heading[2] for heading in headings], ['同步这个镜像仓库', '操作步骤'])
        for document in self.catalog.by_source.values():
            self.assertEqual(len(site.heading_data(site.MD.parse(document.markdown('en')))), len(site.heading_data(site.MD.parse(document.markdown('zh')))), str(document.source))

    def test_search_has_chinese_english_and_editorial_pages(self):
        index = json.loads((self.output / 'search.json').read_text())
        architect = next(doc for doc in index if doc['url'] == '/pstack/skills/architect/')
        self.assertIn('architect', architect['text'].lower())
        self.assertIn('设计', architect['text'])
        self.assertEqual(len(index), len(self.catalog.by_source) + 2)
        self.assertTrue(any(doc['url'] == '/pstack/reference/glossary/' for doc in index))

    def test_stale_translation_fails_before_publishing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('# Changed\n')
            (root / 'translations/zh-CN').mkdir(parents=True)
            (root / 'translations/zh-CN/README.md.json').write_text(json.dumps({'source': 'README.md', 'sha256': 'stale', 'blocks': [{'en': '# Before\n', 'zh': '# 之前\n'}]}))
            with patch.object(site.bilingual, 'sources', return_value=[root / 'README.md']):
                with self.assertRaisesRegex(ValueError, 'stale translation'):
                    site.load_catalog(root)

    def test_html_examples_cannot_execute(self):
        text = '# Safe\n\n<script>alert(1)</script>\n\n<img src="https://example.com/a.png" onerror="alert(1)">\n\n<details><summary>Open</summary>Text</details>\n'
        doc = site.Document(PurePosixPath('example.md'), '/example/', 'about', None, 'Safe', 'Safe', ({'en': text, 'zh': text},))
        content, _ = site.render_document(self.catalog, doc, '/pstack/', 'abc', site.ROOT, self.output, [])
        self.assertNotIn('<script>', content['zh'])
        self.assertNotIn('onerror=', content['zh'])
        self.assertIn('<details>', content['zh'])
        self.assertIn('<summary>Open</summary>', content['zh'])

    def test_link_checker_rejects_broken_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / 'manifest.json').write_text(json.dumps({'base': '/', 'documents': []}))
            (output / 'index.html').write_text('<a href="#missing">broken</a>')
            with self.assertRaisesRegex(ValueError, 'missing anchor'):
                site.verify_site(output)

    def test_build_reruns_and_root_deployment(self):
        first = (self.output / 'guide/01-setup/index.html').read_text()
        site.build_site(self.output, '/pstack/')
        self.assertEqual((self.output / 'guide/01-setup/index.html').read_text(), first)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'public'
            site.build_site(output, '/')
            self.assertIn('href="/guide/01-setup/"', (output / 'index.html').read_text())
            self.assertNotIn('href="/pstack/', (output / 'index.html').read_text())

    def test_unknown_output_is_not_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / 'keep.txt').write_text('important')
            with self.assertRaisesRegex(ValueError, 'not owned'):
                site.build_site(output, '/')
            self.assertEqual((output / 'keep.txt').read_text(), 'important')

    def test_principle_groups_follow_the_mode(self):
        groups = site.principle_groups(self.catalog)
        self.assertEqual([title for title, _ in groups], ['核心原则', '架构', '验证', '委派', '改进工作方式'])
        self.assertEqual({doc.source for _, docs in groups for doc in docs}, {doc.source for doc in self.catalog.section('principles')})


if __name__ == '__main__':
    unittest.main()
