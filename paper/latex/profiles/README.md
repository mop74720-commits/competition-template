# Paper Format Profiles

Profiles separate **scientific content** from **competition-specific document formatting**.

The build driver reads `profiles/<name>.json`. A profile declares:

```json
{
  "name": "generic",
  "entrypoint": "main.tex",
  "engine": "xelatex",
  "required_files": ["main.tex"]
}
```

Use:

```bash
python build.py release --profile generic
```

## Why the CUMCM profile is not hard-coded

CUMCM submission formats and official template files can change between years. The repository therefore does **not** permanently vendor an old third-party `cumcmthesis.cls` as the canonical format.

When the current competition opens:

1. verify the current official rules in `rules/`;
2. obtain/verify the current official LaTeX template if one is provided or explicitly permitted;
3. create `profiles/cumcm-current/`;
4. place an adapter entrypoint at `profiles/cumcm-current/main.tex`;
5. copy `cumcm-current.example.json` to `cumcm-current.json`;
6. update `required_files` to include every official class/style file the adapter needs;
7. build with `--profile cumcm-current`;
8. run the repository submission validator before declaring the paper submission-ready.

A profile may change document class, page layout, cover/header behavior, bibliography style, and other presentation concerns. It must not silently rewrite model assumptions, numerical results, claim-evidence links, or official-rule facts.

## Failure semantics

If a selected profile or one of its declared files is missing, `build.py` fails before compiling. This is intentional: silently falling back to the generic profile could create a technically valid PDF in the wrong competition format.
