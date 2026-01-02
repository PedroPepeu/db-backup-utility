import os
import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console

from .base import DatabaseStrategy

console = Console()


class MySQLStrategy(DatabaseStrategy):
    def backup(self):
        host = self.config.get("host")
        port = self.config.get("port")
        user = self.config.get("user")
        password = self.config.get("password")
        db_name = self.config.get("database")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{db_name}_{timestamp}.sql"
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)

        output_path = backup_dir / filename

        console.print(f"[cyan]Preparing MySQL backup: {db_name}...[/cyan]")

        command = ["mysqldump", "-h", str(host), "-P", str(port), "-u", user, db_name]

        env = os.environ.copy()
        if password:
            env["MYSQL_PWD"] = password

        try:
            with open(output_path, "w") as outfile:
                subprocess.run(
                    command, env=env, stdout=outfile, stderr=subprocess.PIPE, check=True
                )

            console.print(
                f"[bold green]MySQL backup finished with success![/bold green]"
            )
            console.print(f"File saved in: {output_path}")
            return str(output_path)

        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error when running mysqldump:[/bold red]")
            console.print(
                "Verify if MySQL is installed and if the credentials are correct."
            )
            if output_path.exists():
                os.remove(output_path)
            return None

        except FileNotFoundError:
            console.print(
                "[bold red]Error:[/bold red] The command 'mysqldump' was not found in the system."
            )
            console.print(
                "If you wan to test without the MySQL installeed, it is needed to mock."
            )
            return None
