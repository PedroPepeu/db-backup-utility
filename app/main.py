import typer
from rich.console import Console

from app.config import load_config
from app.strategies.mysql import MySQLStrategy

app = typer.Typer(help="Db Backup Utility CLI")
console = Console()


@app.command()
def backup(db_name: str = typer.Option(..., help="Database name is in yaml.")):
    """
    Realize an specific setted database backup.
    Use: python app/main.py backup --db-name my_local_mysql
    """
    config = load_config()

    if db_name not in config["databases"]:
        console.print(
            f"[bold red]Error:[/bold red] DB '{db_name}' was not found in config.yaml."
        )
        raise typer.Exit(code=1)

    db_config = config["databases"][db_name]
    db_type = db_config["type"]

    strategy = None

    if db_type == "mysql":
        strategy = MySQLStrategy(db_config)
    elif db_type == "postgres":
        console.print("[yellow]Postgres not yet implemented.[/yellow]")
        return
    else:
        console.print(f"[red]DB type '{db_type}' not yet supported.[/red]")
        return

    strategy.backup()


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
