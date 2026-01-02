import typer
from rich.console import Console

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


if __name__ == "__main__":
    app()
