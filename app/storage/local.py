import shutil
from pathlib import Path

from rich.console import Console

from .base import StorageStrategy

console = Console()


class LocalStorage(StorageStrategy):
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True, parents=True)

    def save(self, source_path: str, destination_filename: str) -> None:
        destination = self.backup_dir / destination_filename

        console.print(f"[cyan]Saving the file locally in: {destination}...[/cyan]")

        shutil.move(source_path, destination)

        console.print(
            f"[bold green]File saved with success in: {destination}[/bold green]"
        )
