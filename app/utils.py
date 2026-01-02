import gzip
import shutil
from pathlib import Path

from rich.console import Console

console = Console()


def compress_file(file_path: str) -> str:
    """
    Input: file_path
    Process: create an compressed version of the file
    Output: returns the path of the new compressed file
    """
    path = Path(file_path)
    compressed_path = path.with_suffix(path.suffix + ".gz")
    console.print(f"[cyan]Compressing file to: {compressed_path}...[/cyan]")

    with open(path, "rb") as f_in:
        with gzip.open(compressed_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    return str(compressed_path)
