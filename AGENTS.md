# Repository Guidelines

## Project Structure & Module Organization
- `main.py` hosts the Dash app that renders the materials graph from JSON inputs.
- Data lives in `data/materials/*.json` (materials) and optionally `data/derivations/*.json` (links); `data.py` holds a small hard-coded sample set.
- Prompt utilities sit in `prompt_cli.py` (Typer CLI) and `prompt-templates/*.tmpl` (LLM prompt bodies).
- Project metadata and dependencies are declared in `pyproject.toml` with a lock in `uv.lock`.

## Setup, Build, Test, and Development Commands
- Install deps (preferred): `uv sync` (or `python -m venv .venv && source .venv/bin/activate && pip install -e .`).
- Run the Dash app locally: `uv run python main.py` (debug server on default Dash port).
- Prompt helpers: `uv run python prompt_cli.py list-templates`; render a prompt: `uv run python prompt_cli.py render --name single --material copper`.
- Validate JSON inputs when editing data: `python -m json.tool data/materials/new_material.json`.

## Coding Style & Naming Conventions
- Target Python 3.12; follow PEP 8 with 4-space indentation. Keep functions small and prefer explicit variable names.
- Use lowercase identifiers with underscores for material IDs (e.g., `iron_ore`), and keep `label` human-friendly.
- Template files are named `<name>.tmpl`; add new names to `TEMPLATES` in `prompt_cli.py`.
- When extending the Dash UI, prefer clear callbacks, avoid silent exception handling, and document non-obvious data flows with short comments.

## Testing Guidelines
- No automated suite yet; when adding features, include `pytest` tests under `tests/` and run with `uv run pytest`.
- Perform quick smoke tests after data or UI changes: run the app and verify nodes/edges render, tooltips show material info, and prompt rendering works for at least one material.
- For new JSON data, load the app to ensure the graph layout handles the added nodes without overlaps or missing edges.

## Commit & Pull Request Guidelines
- Use concise, imperative commit subjects (history shows short uppercase summaries; prefer descriptive lines like “Add material loader validation”).
- For PRs, include: purpose of the change, affected files/data, screenshots of the graph if UI shifts, and any manual test notes. Link related issues when available.
- Keep PRs small and focused; note if new data files or prompts alter expected graph structure.

## Security & Configuration Tips
- Do not commit API keys or proprietary datasets; this repo assumes static, public-friendly JSON inputs.
- Keep `data/` curated—large or noisy datasets will slow the Dash layout; prefer minimal examples with clear derivations.
