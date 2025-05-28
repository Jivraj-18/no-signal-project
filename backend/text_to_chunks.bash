(
  shopt -s globstar
  for f in ./processed_pdfs_docs/**/*.txt; do
    uvx --from split_markdown4gpt mdsplit4gpt "$f" --model gpt-4o --limit 4096 --separator "===SPLIT===" \
    | sed '1s/^/===SPLIT===\n/' \
    | jq -R -s -c --arg file "$f" '
      split("===SPLIT===")[1:]
      | to_entries
      | map({
          id: ($file + "#" + (.key | tostring)),
          content: .value
        })[]
    '
  done
) | tee chunks.json