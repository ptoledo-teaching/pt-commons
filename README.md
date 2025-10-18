# PT Commons Package

**Version:** 1.1  
**Date:** 2025/04/21  
**Author:** Pedro Toledo Correa  
**License:** MIT License  
**Repository:** [GitHub - pt-latex/pt-commons](https://github.com/ptoledo-teaching/pt-commons)

A comprehensive LaTeX package providing common functionality, styling, and utilities for academic and professional documents. This package serves as a foundation for the PT document class family (pt-article, pt-book, pt-report, pt-slides, pt-letter).

## Features

- **Multi-language Support**: Spanish (default), English, Portuguese, French
- **Automatic Font Configuration**: Fira Sans and Inconsolata with proper scaling
- **Document Metadata Management**: Version control, build counting, author handling
- **Enhanced Tables**: Tabularray-based styling with predefined commands
- **File Tree Visualization**: Icon-based directory structures with FontAwesome
- **Code Formatting**: Automatic minted/verbatim fallback with shell-escape detection
- **Customizable Colors**: PT color palette for consistent branding
- **Watermark Support**: Automatic version/build watermarks
- **Smart List of Contents**: Only displays lists when content exists

## Installation

Place `pt-commons.sty` in your LaTeX project directory or install it in your local texmf tree:

```bash
# Local installation
mkdir -p ~/texmf/tex/latex/pt-commons
cp pt-commons.sty ~/texmf/tex/latex/pt-commons/
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

Your content here...

\end{document}
```

## Package Options

### Language Options

```latex
\usepackage[english]{pt-commons}    % English
\usepackage[spanish]{pt-commons}    % Spanish (default)
\usepackage[portuguese]{pt-commons} % Portuguese
\usepackage[french]{pt-commons}     % French
```

### Code Environment Options

```latex
\usepackage[nominted]{pt-commons}   % Disable minted, use verbatim
```

**Note:** Minted is enabled by default but automatically falls back to verbatim if:
- `minted.sty` is not found
- Shell escape is not enabled (`-shell-escape` flag)

## Document Metadata Commands

### Version Control

```latex
\version{1.0}              % Set document version
\build{auto}               % Auto-increment build number
\build{42}                 % Manual build number
\docversion                % Displays: v1.0
```

Build numbers are automatically tracked in `.buildcount` files and increment on each compilation.

### Title Information

```latex
\title{Main Title}
\titlesub{Subtitle}
\titlesubsub{Sub-subtitle}
\date{2025-10-18}
```

### Academic/Class Information

```latex
\classcode{CS-101}
\classname{Introduction to Computer Science}
\classsemester{Fall 2025}
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
\corporationname{Company Name}
\corporationdepartment{Department Name}
```

## Author Management

Add multiple authors with full details:

```latex
\addauthor{FirstName}{LastName}{email@domain.com}{Affiliation/Details}
\addauthor{Jane}{Doe}{jane@university.edu}{Department of CS, University}
\addauthor{John}{Smith}{john@company.com}{Senior Engineer, Tech Corp}
```

### Author Display Commands

```latex
\titleauthorsnames{, }        % Names separated by comma-space
\titleauthorsfooter{; }       % Names with emails in footer
\titleauthorsboxes            % Authors in centered minipages
\titleauthorsfootnotes        % Affiliations as footnotes
\titleauthorstable            % Authors in table format
```

## Colors

Pre-defined PT color palette:

| Color | Hex Code |
|-------|----------|
| `ptred` | `#D60019` |
| `ptdarkred` | `#68000C` |
| `ptlightblue` | `#499BDA` |
| `ptblue` | `#004B85` |
| `ptdarkblue` | `#002038` |
| `ptgreen` | `#008452` |
| `ptdarkgreen` | `#003823` |
| `ptyellow` | `#F7AE00` |
| `ptdarkyellow` | `#896000` |
| `ptgray` | `#E0E0E0` |
| `ptdarkgray` | `#949494` |

```latex
\textcolor{ptblue}{Blue text}
\colorbox{ptgray}{Gray background}
```

## Tables

Enhanced table commands using tabularray:

```latex
\begin{tblr}{colspec={lcc}}
\tableheader
Header 1 & Header 2 & Header 3 \\
\tablesubheader
Subheader & \tablecellcenter Data & More \\
Regular & \tablecellbold Bold & \tablecellright Right \\
\end{tblr}
```

### Table Commands

- `\tableheader` - Blue header row with bold text
- `\tablesubheader` - Light blue subheader row
- `\tablecellleft` - Left-aligned cell
- `\tablecellcenter` - Center-aligned cell
- `\tablecellright` - Right-aligned cell
- `\tablecellbold` - Bold cell content
- `\tablecellrotated` - Rotated 90° cell content

### Column Types

```latex
L{width}  % Left-aligned with specific width
C{width}  % Center-aligned with specific width
R{width}  % Right-aligned with specific width
X{width}  % Justified with specific width
```

## File Trees

Create visual directory structures with icons:

```latex
\begin{filetree}
\caption{Project Structure}
\begin{ptdirtree}
\dirtree{%
.1 \treeiconfirst{}.
.2 \treeicon{src/}.
.3 \treeicon{main.py}.
.3 \treeicon{utils.py}.
.2 \treeicon{README.md}.
.2 \treeicon{requirements.txt}.
}
\end{ptdirtree}
\end{filetree}
```

Automatically recognizes 50+ file extensions with appropriate FontAwesome icons:
- **Code**: `.py`, `.js`, `.cpp`, `.java`, `.tex`, etc.
- **Documents**: `.pdf`, `.doc`, `.docx`, `.xls`, `.ppt`
- **Archives**: `.zip`, `.tar`, `.gz`, `.7z`
- **Media**: `.jpg`, `.png`, `.mp4`, `.mp3`

## Code Blocks

```latex
\begin{ptprintcode}{python}
def hello_world():
    print("Hello, World!")
\end{ptprintcode}
```

The package automatically:
1. Tries to use `minted` if available and shell-escape is enabled
2. Falls back to `verbatim` with a warning if not
3. Applies syntax highlighting (minted) or plain formatting (verbatim)

To compile with minted support:
```bash
pdflatex -shell-escape document.tex
```

## List of Contents

Smart list commands that only appear if content exists:

```latex
\ptlistoftables    % Only shows if tables exist
\ptlistoffigures   % Only shows if figures exist
\ptlistofcodes     % Only shows if code listings exist
```

## Graphics and Images

### Figure Helper

```latex
\ptfigure{h}{width=0.8\textwidth}{image.png}{Caption text}{label}
% Creates a figure with automatic centering and labeling
```

### Background Images

```latex
\background{background.jpg}
\backgroundcredit{Photo by Author}
```

### Logos

```latex
\logo{logos/university-logo.png}
```

## Watermarks

Add watermarks with version/build information:

```latex
\watermark{DRAFT}
% Automatically includes version and build if defined
% Result: "DRAFT - v1.0.42" (if version and build are set)
```

The watermark:
- Automatically scales to paper size
- Positioned at 45° angle
- Uses `ptred` color at 21% opacity
- Combines with version/build numbers when available

## Utility Commands

```latex
\inlinecode{code}        % Inline code formatting
\todayymd                % Current date as YYYY/MM/DD
\twodigits{5}            % Formats number as "05"
```

### Caption Commands (non-beamer only)

```latex
\ptcaption{figure}{Caption text}      % Add caption outside float
\ptcaptionsame{figure}{Caption text}  % Reuse previous number
```

## Beamer Compatibility

The package automatically detects when used with beamer and:
- Skips geometry package (conflicts with beamer)
- Skips caption customization (beamer handles it)
- Preserves all other functionality

## Dependencies

### Required Packages

- `adjustbox`, `colortbl`, `enumitem`, `etoolbox`, `expl3`
- `float`, `fontawesome5`, `graphicx`, `microtype`
- `newtxsf`, `ragged2e`, `tabularray`, `tcolorbox`
- `textpos`, `xstring`, `babel`, `totcount`
- `dirtree`, `xcolor`, `tikz`, `pgfplots`
- `fancyvrb`, `draftwatermark`, `iftex`
- `hyperref` (loaded with guard for beamer)

### Optional Packages

- `minted` - Enhanced code highlighting (requires `-shell-escape`)
- `listings` - Alternative code formatting

### Fonts

- **Sans-serif**: Fira Sans (scaled 0.85)
- **Monospace**: Inconsolata (scaled 0.85)

## Examples

### Academic Paper

```latex
\documentclass{article}
\usepackage[english]{pt-commons}

\title{Machine Learning Applications}
\titlesub{A Comprehensive Study}
\addauthor{Jane}{Doe}{jane@uni.edu}{CS Dept, University}
\version{1.0}
\build{auto}

\begin{document}
\maketitle
\titleauthorsboxes
\titleauthorsfootnotes

\tableofcontents
\ptlistoffigures
\ptlistoftables

% Content...

\end{document}
```

### Corporate Report

```latex
\documentclass{report}
\usepackage{pt-commons}

\title{Q4 Financial Report}
\corporationname{Tech Solutions Inc.}
\corporationdepartment{Finance Division}
\version{2.1}
\watermark{CONFIDENTIAL}

\begin{document}
% Content...
\end{document}
```

## License

MIT License

Copyright (c) 2025 Pedro Toledo Correa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support

For issues, suggestions, or contributions, please contact the package maintainer or visit the package repository.

---

**Last Updated:** October 2025
