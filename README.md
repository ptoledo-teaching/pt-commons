# PT Commons Package

**Version:** 0.4<br>
**Date:** 2026/08/29<br>
**Author:** Pedro Toledo Correa<br>
**License:** LaTeX Project Public License 1.3c or later<br>
**Repository:** [GitHub - ptoledo-teaching/pt-commons](https://github.com/ptoledo-teaching/pt-commons)

PT Commons provides the shared commands, styles, and runtime helpers used by the
PT document class family (`pt-article`, `pt-report`, `pt-slides`, and
`pt-letter`). It can also be loaded directly from a standard LaTeX class.

## Features

- Multi-language support: Spanish (default), English, Portuguese, and French
- Reusable document, institution, class, and corporate metadata
- Multiple-author formatting with optional email and affiliation information
- Shared PT colors, typography, headers, footers, lists, and section styles
- Tabularray table helpers and TikZ/PGFPlots support
- File-tree floats with Font Awesome icons
- Minted code blocks with an explicit verbatim fallback
- Optional document watermarks and manual or automatic build information
- Conditional lists of figures, tables, and code listings

## Architecture

`pt-commons.sty` is the public facade. Its implementation is split into four
internal modules:

| File | Responsibility |
| --- | --- |
| `pt-commons.sty` | Public package, options, and module loading order |
| `pt-commons-core.sty` | Metadata, languages, links, authors, colors, and semantic commands |
| `pt-commons-layout.sty` | Typography, headers, footers, sections, lists, and visual defaults |
| `pt-commons-content.sty` | Tables, figures, file trees, plots, and code blocks |
| `pt-commons-runtime.sty` | Build metadata, watermarks, and document hooks |

The four implementation modules are internal: documents should continue to
load only `pt-commons`.

PT host classes can use the module-state selectors exposed by the facade:
`\ptiflayoutloaded`, `\ptifcontentloaded`, and `\ptifruntimeloaded`. This avoids
coupling classes to the package's private module switches.

Shared metadata is exposed without revealing its storage macros:
`\ptmetadata{title}` reads a value, `\ptifmetadata{title}{...}{...}` branches
on a non-empty value, and `\ptifmetadatadefined{date}{...}{...}` distinguishes
an omitted setter from an explicitly empty one. Supported keys are `version`,
`build`, `buildsources`, `title`, `date`, `titlesub`, `titlesubsub`, `classcode`,
`classsemester`, `classname`, `workgroup`, `department`, `school`, `university`,
`corporation`, `corporationdepartment`, `background`, `backgroundcredit`,
`logo`, and `watermark`. Unknown keys produce a package error rather than
exposing similarly named implementation macros.

Author-aware hosts can branch with `\ptifauthors{...}{...}`. Shared localized
strings are available in the preamble and document through `\ptlabel{toc}`,
`\ptlabel{questions}`,
`\ptlabel{instruction}`, `\ptlabel{backgroundsource}`, and
`\ptlabel{templatecredit}`.

Run `sh tests/check-core-api.sh` to verify this integration contract with all
three supported engines.

## Installation

All five `.sty` files must remain together. Place them in the document directory
or install them in a local TeX tree:

```bash
mkdir -p ~/texmf/tex/latex/pt-commons
cp pt-commons*.sty ~/texmf/tex/latex/pt-commons/
texhash ~/texmf
```

## Basic Usage

```latex
\documentclass{article}
\usepackage{pt-commons}

\title{My Document}
\author{Your Name}
\date{\today}

\begin{document}
\maketitle

Your content here.

\end{document}
```

The package preserves the standard behavior of `\title` and `\date`, including
Beamer's optional short forms, while also making their values available to the
PT classes.

## Package Options

### Language

```latex
\usepackage[english]{pt-commons}
\usepackage[spanish]{pt-commons}    % Default
\usepackage[portuguese]{pt-commons}
\usepackage[french]{pt-commons}
```

The package also follows later `\selectlanguage{...}` changes.

### Module Loading

The default remains the complete package. Advanced documents and host classes
can disable the optional modules independently:

```latex
\usepackage[coreonly]{pt-commons}              % Core only
\usepackage[nolayout]{pt-commons}              % Core + content + runtime
\usepackage[nocontent]{pt-commons}             % Core + layout + runtime
\usepackage[noruntime]{pt-commons}             % Core + layout + content
\usepackage[coreonly,content]{pt-commons}      % Core + content
```

`minimal` is an alias for `coreonly`; `full` restores all modules. The positive
options `layout`, `content`, and `runtime` can be combined after `coreonly`.
Options are applied from left to right. PT host classes expose namespaced
counterparts such as `ptlayout` and `ptcontent` so these generic package option
names do not leak to unrelated packages; consult each class for its exact API.

Core-only mode retains metadata, languages, authors, colors, links,
`\ptinstruction`, and caption helpers. It does not load PT typography, table and
graphics helpers, Minted, TikZ/PGFPlots, file trees, watermarks, or persistent
build state.

### Code Environment

Minted is enabled by default:

```latex
\begin{ptprintcode}{python}
def hello_world():
    print("Hello, World!")
\end{ptprintcode}
```

Use the explicit fallback when Minted is unavailable or external command
execution is not desired:

```latex
\usepackage[nominted]{pt-commons}
```

If `minted.sty` is not installed, PT Commons automatically uses the verbatim
fallback and issues a warning. Depending on the installed Minted version and
TeX configuration, syntax highlighting may require shell escape:

```bash
pdflatex -shell-escape document.tex
```

The fallback `ptprintcode` accepts the same language argument but renders plain
verbatim text.

## Document Metadata

Metadata setters may be called more than once; the last value is used.

### Version and Build

```latex
\version{1.0}
\build{auto}   % Source-revision build number
\buildsource{chapter-1.tex}  % Also track an included source
\build{42}     % Fixed build number
\docversion    % Prints v1.0, or NA if no version was set
```

Automatic mode stores its state in a job- and version-specific `*.buildcount`
file. No build-count file is read or written when `\build` is omitted or a
manual build value is used.

`\build{auto}` is a source-revision counter: it advances when the fingerprint
of a tracked source changes, not on every TeX pass. The default tracked source
is `\jobname.tex`. Add included files, bibliography files, or other inputs with
repeatable `\buildsource{...}` calls; the main source remains tracked. Use
`\buildsources{file-a.tex,file-b.tex}` to replace the complete list instead.
The order of that list is significant.

When the engine is invoked with `-jobname`, or the main source is outside the
current working directory, `\jobname.tex` may not be its actual path. In that
case, set the complete list explicitly with `\buildsources{path/main.tex,...}`.

A new state starts at B0. Existing one-line state files are migrated without
changing their number. If a tracked source cannot be found, the current number
is frozen and a warning explains which source must be corrected. The state is
rewritten only when its fingerprint changes, so Latexmk converges normally and
no `latexmkrc` ignore rule is required. Avoid concurrent compilations that
share the same job name and state file.

### Title

```latex
\title{Main Title}
\titlesub{Subtitle}
\titlesubsub{Sub-subtitle}
\date{2026-08-28}
```

### Academic and Class Information

```latex
\classcode{CS-101}
\classname{Introduction to Computer Science}
\classsemester{Fall 2026}
```

### Institution Information

```latex
\university{University Name}
\school{School of Engineering}
\department{Computer Science Department}
\workgroup{Research Group Name}
```

### Corporate Information

```latex
\corporation{Company Name}
\corporationdepartment{Department Name}
```

## Author Management

Add authors as first name, last name, email, and affiliation/details:

```latex
\addauthor{Jane}{Doe}{jane_one@university.edu}{Department of CS}
\addauthor{John}{Smith}{}{Senior Engineer}
```

Emails and details may be empty. The author renderers do not display empty
parentheses or footnotes.

```latex
\titleauthorsnames{, }   % Names separated by comma-space
\titleauthorsfooter{; }  % Names and non-empty emails
\titleauthorsboxes       % Centered author minipages
\titleauthorsfootnotes   % Affiliations as footnotes
\titleauthorstable       % Natural-width table; wraps only when needed
```

`\titleauthorstable` keeps its natural width when it fits the available line
and switches to a wrapping `tabularx` only for oversized author data. The host
class chooses whether that table is centered or right-aligned.

## Colors

| Color | Hex |
| --- | --- |
| `ptred` | `#D60019` |
| `ptredlight` | `#FF4962` |
| `ptdarkred` | `#68000C` |
| `ptlightblue` | `#499BDA` |
| `ptblue` | `#004B85` |
| `ptdarkblue` | `#002038` |
| `ptgreen` | `#008452` |
| `ptgreenlight` | `#49DA9B` |
| `ptdarkgreen` | `#003823` |
| `ptyellow` | `#F7AE00` |
| `ptyellowlight` | `#FFD549` |
| `ptdarkyellow` | `#896000` |
| `ptgray` | `#E0E0E0` |
| `ptdarkgray` | `#949494` |

```latex
\textcolor{ptblue}{Blue text}
\colorbox{ptgray}{Gray background}
```

## Tables

```latex
\begin{tblr}{colspec={lcc}}
\tableheader
Header 1 & Header 2 & Header 3 \\
\tablesubheader
Subheader & \tablecellcenter Data & More \\
Regular & \tablecellbold Bold & \tablecellright Right \\
\end{tblr}
```

Available table commands are `\tableheader`, `\tablesubheader`,
`\tablecellleft`, `\tablecellcenter`, `\tablecellright`, `\tablecellbold`, and
`\tablecellrotated`. PT Commons provides these column forms as part of its
public table API:

- `L`, `C`, and `R` create flexible top-aligned columns with left, centered,
  and right-aligned text.
- `L{4cm}`, `C{4cm}`, and `R{4cm}` create fixed-width aligned columns.
- `X`, `X[2]`, `X[l]`, and `X[l,wd=4cm]` create flexible or
  key-configured columns.
- `X{4cm}` and `X[l]{4cm}` create fixed-width justified or left-aligned
  columns.

The underlying native `Q` forms are also available:
`Q[l,t,co=1]` is flexible and `Q[l,t,wd=4cm]` has a fixed width. If a host
document registers its own `L`, `C`, or `R` type before loading PT Commons,
that definition is left unchanged.

These forms are the established PT Commons API. Tabularray does not expose a
public definition operation capable of expressing the optional braced width
or the complete PT `X` grammar, so the content module keeps the required
column-parser integration isolated and checks that the parser API is available.
Run `sh tests/check-table-columns.sh` for the PDFLaTeX contract check, or append
`xelatex lualatex` to test all three engines. The runner also checks that
host-defined column types remain untouched.

## File Trees

```latex
\begin{filetree}
\caption{Project Structure}
\begin{ptdirtree}
\dirtree{%
.1 \treeiconfirst{}.
.2 \treeicon{src/}.
.3 \treeicon{main.py}.
.2 \treeicon{README.md}.
}
\end{ptdirtree}
\end{filetree}
```

Known archive, audio, code, office, image, PDF, and video extensions receive a
matching Font Awesome icon. Extension matching is case-insensitive and uses the
last suffix, so names such as `archive.tar.GZ` work. A trailing `/` denotes a
folder. Extensionless names preserve the historical folder heuristic; use
`\treeicon[file]{LICENSE}` or `\treeicon[folder]{dir.v1}` to resolve ambiguous
names explicitly. The same optional selector is available on `\treeiconfirst`.
File-tree captions use their own auxiliary list and therefore do not appear in
the list of figures.

## Lists of Contents

These commands print a list only when the corresponding counter is nonzero:

```latex
\ptlistoftables
\ptlistoffigures
\ptlistofcodes
```

## Graphics

```latex
\ptfigure{h}{width=.8\textwidth}{image.png}{Caption}{sample}
\ptfigure{h}{width=.8\textwidth}{image.png}{Caption}{fig:sample}
```

Both calls create the label `fig:sample`; the `fig:` prefix is optional.

```latex
\background{background.jpg}
\backgroundcredit{Photo by Author}
\logo{logos/university-logo.png}
```

## Watermarks

```latex
\watermark{DRAFT}
```

When version and build metadata exist, they are appended to the watermark. An
empty watermark is ignored. PT Commons scales the result to the page, rotates it
45 degrees, and uses `ptred` at 21% opacity.

## Utility Commands

```latex
\inlinecode{code}
\inlinecode{bucket-<normalized-id>}
\inlinecode{~/.ssh/id_ed25519}
\ptinstruction{Review the results.}
\todayymd
\twodigits{5}  % 05
```

Plain `\inlinecode` content treats code punctuation literally, including `~`,
`_`, `<`, and `>`, so these characters do not require LaTeX escapes.

`\ptinstruction` uses the active language and is the generic public command for
highlighting instructions to the document user.

Caption helpers are available in both standard classes and Beamer:

```latex
\ptcaption{figure}{Caption text}
\ptcaptionsame{figure}{Caption text}
```

`\ptcaptionsame` reuses the current number while creating a distinct hyperlink
target. If no earlier caption of that type exists, it creates the first one and
issues a warning instead of producing number zero.

## Beamer Compatibility

When Beamer is detected, PT Commons avoids packages that conflict with the
class, including `geometry`, `caption`, `fancyhdr`, `titlesec`, and `enumitem`.
It preserves Beamer's optional `\title[short]{long}` and `\date[short]{long}`
forms.

## Dependencies

PT Commons requires LaTeX 2023-06-01 or newer.

Dependencies are scoped by module:

- Core: `babel`, `caption` or `capt-of`, `etoolbox`, `expl3`, `hyperref`,
  `letltxmacro`, `tabularx`, and `xcolor`.
- Layout: `enumitem`, `fancyhdr`, `iftex`, `microtype`, `newtxsf`, `titlesec`,
  Fira Sans, and Bera Mono or Fira Mono.
- Content: `colortbl`, `dirtree`, `fancyvrb`, `float`, `fontawesome5`,
  `graphicx`, `pgfplots`, `tabularray`, `tcolorbox`, `tikz`, and `totcount`.
- Runtime: `draftwatermark`.

Class-sensitive packages are loaded only where applicable. `minted` is optional
and belongs to the content module.

The configured text font is Fira Sans (scaled to 0.85). The monospaced font is
Bera Mono under PDFLaTeX and Fira Mono under XeLaTeX or LuaLaTeX, scaled to 0.8.

## License

This work may be distributed and/or modified under the conditions of the LaTeX
Project Public License, version 1.3c or later. See
<https://www.latex-project.org/lppl.txt>.

## Support

For issues, suggestions, or contributions, contact the package maintainer or
visit the package repository.

---

**Last Updated:** August 2026
