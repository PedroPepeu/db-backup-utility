import typer
from rich.console import Console

from app.config import load_config

app = typer.Typer(help="Db Backup Utility CLI")
console = Console()


@app.command()
def backup():
    """
    Future command to realize backup
    """
    console.print("[green]Starting backup process... (Simulating)[/green]")


@app.command()
def restore():
    """
    Future command to realize rollback
    """
    console.print("[yellow]Starting rollback process... (Simulating)[/yellow]")


@app.command()
def version():
    """
    Tool version
    """
    console.print("DB Backup CLI v0.1.0", style="bold blue")


@app.command()
def check_config():
    """
    Validate and show the loaded configs
    """
    config = load_config()
    console.print("[bold green]Config loaded with success![/bold green]")
    console.print(f"Dir of backup: {config['general']['backup_dir']}")
    console.print("DB Setted:")
    for db_name, db_info in config["databases"].items():
        console.print(f" - [cyan]{db_name}[/cyan] ({db_info['type']})")


if __name__ == "__main__":
    app()
