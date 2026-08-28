# PT Commons Package

**Version:** 0.2<br>
**Date:** 2026/08/28<br>
**Author:** Pedro Toledo Correa<br>
**License:** LaTeX Project Public License 1.3c or later<br>
**Repository:** [GitHub - pt-latex/pt-commons](https://github.com/ptoledo-teaching/pt-commons)

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
| `pt-commons-core.sty` | Dependencies, metadata, languages, links, authors, and colors |
| `pt-commons-layout.sty` | Headers, footers, sections, lists, and text styles |
| `pt-commons-content.sty` | Tables, figures, file trees, plots, and code blocks |
| `pt-commons-runtime.sty` | Build metadata, watermarks, and document hooks |

The four implementation modules are internal: documents should continue to
load only `pt-commons`.

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
\build{auto}   % Persistent automatic build number
\build{42}     % Fixed build number
\docversion    % Prints v1.0, or NA if no version was set
```

Automatic mode stores its state in a job- and version-specific `*.buildcount`
file. No build-count file is read or written when `\build` is omitted or a
manual build value is used. The automatic value advances once per TeX engine
pass.

Because `*.buildcount` is both read and rewritten, Latexmk must ignore changes
to that file when deciding whether another pass is necessary. Add this rule to
the project's `latexmkrc`:

```perl
$hash_calc_ignore_pattern{'buildcount'} = '^';
```

Without the rule, `\build{auto}` can keep Latexmk running until its maximum
number of passes. A fixed `\build{...}` value needs no special configuration.

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
\titleauthorstable       % Authors in tabular form
```

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
`\tablecellrotated`. The `L`, `C`, `R`, and `X` column types accept either
automatic width or an explicit braced width, such as `L{4cm}`.

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
matching Font Awesome icon. File-tree captions use their own auxiliary list and
therefore do not appear in the list of figures.

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
\ptinstruction{Review the results.}
\todayymd
\twodigits{5}  % 05
```

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

Required packages include:

- `adjustbox`, `babel`, `caption` or `capt-of`, `colortbl`, `dirtree`
- `draftwatermark`, `enumitem`, `etoolbox`, `expl3`, `fancyhdr`, `fancyvrb`
- `FiraSans`, `FiraMono` or `beramono`, `fix-cm`, `float`, `fontawesome5`, `geometry`, `graphicx`, `hyperref`, `iftex`
- `letltxmacro`, `microtype`, `newtxsf`, `pgfplots`, `ragged2e`
- `tabularray`, `tcolorbox`, `textpos`, `tikz`, `titlesec`, `totcount`, `xcolor`, `xstring`

Class-sensitive packages are loaded only where applicable. `minted` is optional.

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
