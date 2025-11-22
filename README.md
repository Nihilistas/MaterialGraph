## Glosary
# Material - a harnessable physical substance, that can be used to make things

## Goal
# Find an easy to comprehend way to visualize and learn about materials. Examples of types of data:
1. Which are derived from which (wood->paper, grass->paper)
2. Where can you find it (in nature, synthesized)
3. Ways to find it (location, time of year, appearance)
4. Ways to make it (step-by-step recipe/algorithm)

## Generating data with codex exec
- Render a prompt, run it through `codex exec`, and save the JSON directly with the helper script:
  - `sh research single copper` → writes `data/materials/copper.json`
  - `sh research derivation copper` → writes `data/derivations/copper.json`
  - `sh research batch materials.txt` → writes `data/materials/batch_materials.json` (use an optional 3rd arg for a different filename)
- Requirements: `codex exec` on PATH and `uv` to run `prompt_cli.py`.
