#!/bin/sh
set -eu

test_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test_repo_dir=$(dirname -- "$test_script_dir")
test_output_dir=$(mktemp -d /tmp/pt-commons-table-columns.XXXXXX)
test_cache_dir="$test_output_dir/texmf-cache"
test_problem_pattern='(^!|LaTeX Error|Package .* Error|Unknown Column|Overfull \\[hv]box|Unexpandable command|Missing number)'
mkdir -p "$test_cache_dir"

if [ "$#" -eq 0 ]; then
    set -- pdflatex
fi

for test_engine in "$@"; do
    if ! command -v "$test_engine" >/dev/null 2>&1; then
        echo "Missing TeX engine: $test_engine" >&2
        exit 1
    fi

    test_engine_name=${test_engine##*/}
    for test_source in table-columns table-host-column; do
        test_job_name="$test_source-$test_engine_name"
        test_log="$test_output_dir/$test_job_name.log"

        if ! env \
            TEXINPUTS="$test_repo_dir:" \
            TEXMFCACHE="$test_cache_dir" \
            TEXMFVAR="$test_cache_dir" \
            XDG_CACHE_HOME="$test_cache_dir" \
            "$test_engine" \
            -interaction=nonstopmode \
            -halt-on-error \
            -output-directory="$test_output_dir" \
            -jobname="$test_job_name" \
            "$test_script_dir/$test_source.tex" >/dev/null; then
            echo "$test_engine failed while compiling $test_source.tex" >&2
            if [ -f "$test_log" ]; then
                tail -n 50 "$test_log" >&2
            fi
            exit 1
        fi

        if grep -Eq "$test_problem_pattern" "$test_log"; then
            echo "$test_engine violated the table API in $test_source.tex:" >&2
            grep -En "$test_problem_pattern" "$test_log" >&2
            exit 1
        fi
    done
done

echo "Table column API checks passed: $*"
echo "Test artifacts: $test_output_dir"
