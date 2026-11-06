---
layout: single
title: Code rendering check
author_profile: false
permalink: /code-rendering-check/
---

Inline `echo "hello"` stays inline.

```sh
# Shell comment
printf '%s\n' "<script>alert('code')</script> & shell"
printf '%s\n' "A long line stays on one line: 0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz"
```

```python
# Python comment
def greet(name):
    return f"Hello, {name}: <tag> & text", 42
```

```text
<tag attr="value"> & plain text
    four spaces
	one tab
```

```
<unlabelled> & plain
```

<details markdown="1">
<summary>Optional commands</summary>

Inside **the disclosure**.

```sh
# Disclosure comment
printf '%s\n' "</details><script>alert('code')</script> & inside"
```

</details>

## After the disclosure

Outside **the disclosure**.

<div>
**Unparsed HTML stays literal.**
</div>
