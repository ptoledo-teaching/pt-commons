#!/usr/bin/env python3
"""Verify Commons' localized text without depending on any PT host class."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]
OUT = Path(tempfile.mkdtemp(prefix='pt-commons-localized-text.'))
ENGINES = sys.argv[1:] or ['pdflatex', 'xelatex', 'lualatex']
ENV = os.environ.copy()
ENV.update(TEXINPUTS=f'{REPO}:', TEXMFCACHE=str(OUT / 'cache'), TEXMFVAR=str(OUT / 'cache'), XDG_CACHE_HOME=str(OUT / 'cache'), max_print_line='1000')
(OUT / 'cache').mkdir()
LANGUAGES = ['spanish', 'english', 'portuguese', 'french']
PROBLEMS = re.compile(r'Undefined control sequence|Missing character:|LaTeX Error|Package .* Error|Overfull \\[hv]box|Token not allowed in a PDF string')


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def document(body, language='english', preamble='', host='article'):
    options = 'coreonly' + (',' + language if language else '')
    if host == 'beamer':
        body = r'\begin{frame}' + body + r'\end{frame}'
    return (rf'\documentclass{{{host}}}\usepackage[{options}]{{pt-commons}}' + '\n' + preamble + '\n' + r'\begin{document}' + '\n' + body + '\n' + r'\end{document}')


def selected(language, marker):
    values = ','.join(l + '={' + (marker if l == language else r'\UndefinedInactiveCommand') + '}' for l in LANGUAGES)
    return r'\pttext{' + values + '}'


def compile_case(engine, name, source, expected=None, error=None):
    folder = OUT / engine / name
    folder.mkdir(parents=True)
    (folder / 'case.tex').write_text(source)
    for run in range(1 if error else 2):
        result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', '-no-shell-escape', '-file-line-error', 'case.tex'], cwd=folder, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (folder / f'pass-{run}.console').write_bytes(result.stdout)
        log = (folder / 'case.log').read_text(errors='replace')
        if error:
            check(result.returncode != 0, f'{name}: expected an error')
            normalized = ' '.join(log.split())
            check('Package pt-commons Error:' in normalized and error in normalized, f'{name}: missing Commons diagnostic {error!r}; see {folder}')
            print(f'[{engine}] {name}: expected error', flush=True)
            return
        check(result.returncode == 0 and not PROBLEMS.search(log), f'{name}: compilation failed; see {folder}')
    for package in ['pt-commons-layout.sty', 'pt-commons-content.sty', 'pt-commons-runtime.sty', 'minted.sty']:
        check(package not in log, f'{name}: core-only mode loaded {package}')
    text = subprocess.check_output(['pdftotext', str(folder / 'case.pdf'), '-']).decode()
    for marker in expected or []:
        check(marker in text, f'{name}: missing {marker!r}')
    check('INACTIVE' not in text, f'{name}: unselected text leaked')
    print(f'[{engine}] {name}: OK', flush=True)


try:
    for command in ENGINES + ['pdftotext']:
        check(shutil.which(command), f'Required command not found: {command}')
    for engine in ENGINES:
        for language in LANGUAGES:
            compile_case(engine, language, document(selected(language, language.upper()), language), [language.upper()])
        compile_case(engine, 'default-spanish', document(selected('spanish', 'DEFAULTSPANISH'), None), ['DEFAULTSPANISH'])
        switches = selected('english', 'INITIALENGLISH')
        for language in ['spanish', 'portuguese', 'french']:
            switches += r'\par{\selectlanguage{' + language + '}' + selected(language, 'LOCAL' + language.upper()) + '}'
        switches += r'\par' + selected('english', 'RESTOREDENGLISH')
        locales = ''.join(r'\babelprovide[import]{' + language + '}' for language in ['spanish', 'portuguese', 'french'])
        compile_case(engine, 'language-scopes', document(switches, preamble=locales), ['INITIALENGLISH', 'LOCALSPANISH', 'LOCALPORTUGUESE', 'LOCALFRENCH', 'RESTOREDENGLISH'])
        nested = r'\pttext{english={OUTER \pttext{english={INNER},spanish={\UndefinedInactiveCommand}} END},french={\UndefinedInactiveCommand}}\par\pttext{english={NEXT},spanish={}}'
        compile_case(engine, 'nested-and-independent', document(nested), ['OUTER', 'INNER', 'END', 'NEXT'])
        rich = r'\pttext{english={\textbf{BOLD}, \href{https://example.org}{LINK}\par SECOND PARAGRAPH},spanish={\UndefinedInactiveCommand}}'
        compile_case(engine, 'rich-text', document(rich), ['BOLD', 'LINK', 'SECOND PARAGRAPH'])
        moving = r'\tableofcontents\section{\texorpdfstring{\pttext{english={SECTION},spanish={INACTIVE}}}{SECTION}}\pttext{english={BODY}}'
        compile_case(engine, 'moving-argument', document(moving), ['SECTION', 'BODY'])
        for host in ['report', 'beamer']:
            compile_case(engine, host, document(selected('english', 'HOSTTEXT'), host=host), ['HOSTTEXT'])
        errors = {
            'missing': (r'\pttext{spanish={Texto}}', "Missing inline translation 'english'"),
            'empty-set': (r'\pttext{}', "Missing inline translation 'english'"),
            'empty-selected': (r'\pttext{english={ }}', "Missing inline translation 'english'"),
            'duplicate-selected': (r'\pttext{english={A},english={B}}', "Duplicate translation 'english'"),
            'duplicate-inactive': (r'\pttext{english={A},spanish={B},spanish={C}}', "Duplicate translation 'spanish'"),
            'unknown-inactive': (r'\pttext{english={A},engish={B}}', "Unsupported language 'engish'"),
            'valueless': (r'\pttext{english}', "Missing translation value for 'english'"),
            'valueless-inactive': (r'\pttext{english={A},spanish}', "Missing translation value for 'spanish'"),
        }
        for name, (body, error) in errors.items():
            compile_case(engine, name, document(body), error=error)
        compile_case(engine, 'unsupported-active-language', document(r'\pttext{english={A}}', preamble=r'\AtBeginDocument{\def\languagename{unsupported}}'), error="Unsupported language 'unsupported'")
    print('Localized text checks passed: ' + ', '.join(ENGINES))
except (AssertionError, subprocess.CalledProcessError) as error:
    print(f'FAIL: {error}', file=sys.stderr)
    sys.exit(1)
finally:
    print(f'Test artifacts: {OUT}', flush=True)
