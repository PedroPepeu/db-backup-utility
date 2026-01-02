import os

import typer
from rich.console import Console

from app.config import load_config
from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage
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

    backup_file_path = strategy.backup()

    if not backup_file_path:
        console.print("[bold red]Fail in backup. Aborting upload...[/bold red]")
        raise typer.Exit(code=1)

    storage_type = config["general"].get("storage_type", "local")
    storage = None

    filename = os.path.basename(backup_file_path)

    if storage_type == "local":
        backup_dir = config["general"]["backup_dir"]
        storage = LocalStorage(backup_dir)

    elif storage_type == "s3":
        aws_conf = config.get("aws", {})
        storage = S3Storage(
            bucket_name=aws_conf.get("bucket_name"),
            region=aws_conf.get("region"),
            access_key=aws_conf.get("access_key"),
            secret_key=aws_conf.get("secret_key"),
        )
    else:
        console.print(f"[red]Storage type '{storage_type}' not supported.[/red]")
        return

    storage.save(backup_file_path, filename)


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
