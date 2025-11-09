import json
import typer
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent / "prompt-templates"

def load_template(name: str) -> str:
    """
    Load a template file from the templates folder.
    Template files are named <name>.tmpl
    """
    template_path = TEMPLATE_DIR / f"{name}.tmpl"
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{name}' not found at: {template_path}")

    return template_path.read_text()


app = typer.Typer()

TEMPLATES = {
    "single": "Produce a knowledge-base entry for the material {MATERIAL} in the following exact JSON structure: ",
    "batch": "Template B description…",
    "derivation": "Template C description…",
    "discovery": "Template D description…",
    "recipe": "Template E description…",
    "fill": "Template F description…"
}


@app.command()
def list_templates():
    """List available templates."""
    for name in TEMPLATES:
        typer.echo(f"- {name}")


@app.command()
def show(name: str):
    """Show a template's raw prompt text."""
    if name not in TEMPLATES:
        typer.echo("Unknown template")
        raise typer.Exit(1)
    typer.echo(load_template(name))


@app.command()
def render(
    name: str,
    material: str = typer.Option(None),
    list_file: Path = typer.Option(None),
    existing_file: Path = typer.Option(None),
):
    """
    Render a template with dynamic variables.
    """
    try:
        template = load_template(name)
    except FileNotFoundError as e:
        typer.echo(str(e))
        raise typer.Exit(1)

    # Inject variables
    if material:
        template = template.replace("{MATERIAL}", material)

    if list_file:
        items = list_file.read_text().splitlines()
        template = template.replace("{LIST_OF_MATERIALS}", ", ".join(items))

    if existing_file:
        data = existing_file.read_text()
        template = template.replace("{EXISTING_DATA}", data)

    typer.echo("=== GENERATED PROMPT ===\n")
    typer.echo(template)
    

if __name__ == "__main__":
    app()
