#!/bin/sh
set -eu

test_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test_repo_dir=$(dirname -- "$test_script_dir")
test_output_dir=$(mktemp -d /tmp/pt-commons-core-api.XXXXXX)
test_cache_dir="$test_output_dir/texmf-cache"
test_problem_pattern='(^!|LaTeX Error|Package .* Error|Undefined control sequence|Overfull \\[hv]box|Emergency stop|Fatal error)'
mkdir -p "$test_cache_dir"

if [ "$#" -eq 0 ]; then
    set -- pdflatex xelatex lualatex
fi

for test_engine in "$@"; do
    if ! command -v "$test_engine" >/dev/null 2>&1; then
        echo "Missing TeX engine: $test_engine" >&2
        exit 1
    fi

    test_engine_name=${test_engine##*/}
    test_job_name="core-api-$test_engine_name"
    test_log="$test_output_dir/$test_job_name.log"

    if ! env \
        TEXINPUTS="$test_repo_dir:" \
        TEXMFCACHE="$test_cache_dir" \
        TEXMFVAR="$test_cache_dir" \
        XDG_CACHE_HOME="$test_cache_dir" \
        "$test_engine" \
        -interaction=nonstopmode \
        -halt-on-error \
        -no-shell-escape \
        -output-directory="$test_output_dir" \
        -jobname="$test_job_name" \
        "$test_script_dir/core-api.tex" >/dev/null; then
        echo "$test_engine failed while compiling core-api.tex" >&2
        if [ -f "$test_log" ]; then
            tail -n 60 "$test_log" >&2
        fi
        exit 1
    fi

    if grep -Eq "$test_problem_pattern" "$test_log"; then
        echo "$test_engine produced a fatal diagnostic in core-api.tex:" >&2
        grep -En "$test_problem_pattern" "$test_log" >&2
        exit 1
    fi

    for test_marker in \
        'PT-CORE-AUTHORS-BEFORE=empty' \
        'PT-CORE-AUTHORS-AFTER=present' \
        'PT-CORE-LABEL-PREAMBLE=Table of Contents' \
        'PT-CORE-LAYOUT=off' \
        'PT-CORE-CONTENT=off' \
        'PT-CORE-RUNTIME=off' \
        'PT-CORE-TITLE=present' \
        'PT-CORE-DATE=defined-empty' \
        'PT-CORE-LABEL-TOC=Table of Contents' \
        'PT-CORE-LABEL-QUESTIONS=Questions?' \
        'PT-CORE-LABEL-SPANISH=Tabla de contenidos' \
        'PT-CORE-LABEL-ENGLISH=Table of Contents'
    do
        if ! grep -Fq "$test_marker" "$test_log"; then
            echo "$test_engine did not emit expected marker: $test_marker" >&2
            exit 1
        fi
    done

    test_invalid_job="metadata-invalid-$test_engine_name"
    test_invalid_log="$test_output_dir/$test_invalid_job.log"
    if env \
        TEXINPUTS="$test_repo_dir:" \
        TEXMFCACHE="$test_cache_dir" \
        TEXMFVAR="$test_cache_dir" \
        XDG_CACHE_HOME="$test_cache_dir" \
        "$test_engine" \
        -interaction=nonstopmode \
        -halt-on-error \
        -no-shell-escape \
        -output-directory="$test_output_dir" \
        -jobname="$test_invalid_job" \
        "$test_script_dir/metadata-invalid.tex" >/dev/null 2>&1; then
        echo "$test_engine accepted an unknown metadata key" >&2
        exit 1
    fi
    if ! grep -Fq "Package pt-commons Error: Unknown metadata key \`language'." \
        "$test_invalid_log"; then
        echo "$test_engine did not report the expected unknown-key error" >&2
        exit 1
    fi
done

echo "Core integration API checks passed: $*"
echo "Test artifacts: $test_output_dir"
