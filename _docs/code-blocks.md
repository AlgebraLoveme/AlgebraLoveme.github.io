# Markdown code blocks

Use fenced Markdown with a Rouge language name, such as `sh` or `python`:

````markdown
```sh
printf '%s\n' "Hello, world"
```
````

Use `text` (or omit the language) for unhighlighted output. Preserve indentation
and literal characters inside fences; do not HTML-escape code yourself. Long
lines scroll horizontally rather than wrapping. Inline code still uses single
backticks.

For a disclosure, opt in only its container with `markdown="1"`, keep the summary
as HTML, and leave blank lines around the fence and closing tag:

````markdown
<details markdown="1">
<summary>Optional commands</summary>

```sh
echo "Hello, world"
```

</details>

Ordinary Markdown resumes here.
````

Do not enable global `parse_block_html`. Fences escape HTML, but Liquid runs
before Markdown: wrap examples containing literal Liquid delimiters in
`{% raw %}` / `{% endraw %}` tags. No hand-written highlighting spans or browser
syntax library is needed; the existing Kramdown/GFM and Rouge pipeline handles it.

## Regression check

With the repository's declared gems available, run:

```sh
bundle exec ruby _tests/code_rendering.rb
```

The check uses the real site Markdown configuration
and the non-published fixture in `_tests/fixtures/code-blocks.md`. It checks token
markup, literal text/escaping, whitespace, disclosure boundaries, and the actual
Team disclosure. Browser checks should also cover a narrow viewport, local
horizontal scrolling, and keyboard disclosure toggling with the shared CSS.
