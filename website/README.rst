PStack learning pages
=====================

The site publishes every source returned by ``scripts/bilingual.py``. Original
Markdown and ``translations/zh-CN`` remain authoritative. The two editorial
notes in ``docs/bilingual`` are published separately and excluded from the
translation coverage count. Website maintenance files use reStructuredText so
they do not enter the Markdown translation inventory.

Build and preview
-----------------

Use Python 3.9 or newer. Keep the virtual environment and output outside the
source tree, or put generated files under the excluded ``.translation-work``.

::

    python3 -m venv /tmp/pstack-pages-venv
    /tmp/pstack-pages-venv/bin/pip install -r website/requirements.txt
    /tmp/pstack-pages-venv/bin/python scripts/bilingual.py check
    /tmp/pstack-pages-venv/bin/python -m unittest discover -s scripts -p 'test_site.py' -v
    /tmp/pstack-pages-venv/bin/python scripts/site.py build --base / --output /tmp/pstack-preview
    /tmp/pstack-pages-venv/bin/python -m http.server 8000 --directory /tmp/pstack-preview

Open http://localhost:8000/. To reproduce the GitHub project prefix, build with
``--base /pstack/ --output /tmp/pstack-preview-root/pstack`` and serve
``/tmp/pstack-preview-root``. Refreshing a deep URL works because every route
has its own ``index.html``. Rerunning a build replaces only an output directory
with this generator's manifest. Failed builds leave the previous output intact.

Ordinary builds are offline. They verify source hashes and complete translations,
then check all generated local targets, fragments and duplicate IDs. The build
emits ``manifest.json`` with source-to-route coverage, version provenance and
existing source link defects. ``check --output PATH`` can verify an existing
artifact separately. The current source has one placeholder target, ``url``, in
the synthesizer prompt. It is reported rather than counted as a site page.

Content and routes
------------------

``Catalog`` owns the source and route registries. ``Document`` carries its
section, owner, titles and aligned translation blocks. The renderer joins each
language into one Markdown stream before parsing. Chinese chunks receive blank
line separators, since translation records need not retain trailing newlines.
Safe HTML includes details, tables and images; executable tags and attributes
are escaped or removed. Frontmatter is omitted from reading content.

Directory routes reflect the domain. Guides retain chapter order, skills and
principles have separate indexes, and execution playbooks live under
``/playbooks/``. Reference pages retain their owner path. Principles use the
categories already declared in poteto-mode. Other documents remain accessible
through their collection and the search index. ``/changes/`` contains both
upstream histories. ``/reference/glossary/`` and ``/reference/source-notes/``
are the Chinese editorial notes.

English heading slugs are canonical in both reading languages. Chinese headings
own the plain IDs and English headings use ``en-`` IDs. JavaScript resolves a
canonical fragment to the visible language and opens enclosing details. The
bilingual view presents the complete Chinese document followed by the complete
English document. This preserves nested lists, tables and details without
splitting the Markdown syntax into translation chunks. With JavaScript disabled,
Chinese articles and all site navigation still work. Search and language
switching require JavaScript. Search supports Chinese substrings and English
words locally, with no external search provider.

Updating provenance and upstream history
----------------------------------------

After importing and reviewing a new source version, update
``website/content-provenance.json``. Record the included independent repository
commit, the original Cursor subtree import commit, and the plugin version. The
build verifies the independent commit is an ancestor of HEAD and the version
matches the plugin manifest. A full git history is required.

Fetch metadata explicitly when needed.

::

    /tmp/pstack-pages-venv/bin/python scripts/site.py refresh-upstream

An optional ``GITHUB_TOKEN`` avoids anonymous API rate limits. This command
fetches the last 30 commits from ``backnotprop/pstack`` and the last 30 commits
that touch ``pstack`` in ``cursor/plugins``. It atomically replaces
``website/upstream.json`` only after both requests succeed. Commit the snapshot
with reviewed changes. A metadata refresh never merges sources, rewrites
translations, or changes the recorded imported version.

Publishing
----------

``.github/workflows/pages.yml`` checks pull requests and uploads a preview
artifact without deploying. Main pushes, manual runs and the daily schedule
refresh both upstream histories, build, verify, and deploy to GitHub Pages.
The deployment job runs only on main. The schedule refreshes the deployed
artifact without committing metadata to the repository. Configure the
repository's Pages source as GitHub Actions before the first authorized deploy.
The Pages action supplies the deployment base, including a custom-domain root.

The site does not claim newly fetched upstream commits are translated. It shows
published version, import baselines, check timestamps and bounded commit lists
separately, with links to the full upstream histories and comparisons.
