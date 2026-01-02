from pathlib import Path

import typer
import yaml
from rich.console import Console

console = Console()

CONFIG_FILE = "config.yaml"


def load_config():
    """
    Input: (reads) the config.yaml
    Output: Dictionary
    """
    config_path = Path(CONFIG_FILE)

    if not config_path.exists():
        console.print(f"[bold red]Error:[/bold red] File '{CONFIG_FILE}' not found!")
        console.print(
            "Create the arquive in the root of the project based on the sample."
        )
        raise typer.Exit(code=1)

    with open(config_path, "r") as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as exc:
            console.print(f"[bold red]Error reading YAML:[/bold red] {exc}")
            raise typer.Exit(code=1)
