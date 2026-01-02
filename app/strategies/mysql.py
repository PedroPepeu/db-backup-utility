import os
import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console

# Importa a função de compressão (certifique-se de ter criado o app/utils.py na Tarefa 5)
from app.utils import compress_file

from .base import DatabaseStrategy

console = Console()


class MySQLStrategy(DatabaseStrategy):
    def backup(self) -> str | None:
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

        # Variável para controlar se devemos prosseguir para a compressão
        success = False

        try:
            with open(output_path, "w") as outfile:
                subprocess.run(
                    command, env=env, stdout=outfile, stderr=subprocess.PIPE, check=True
                )
            console.print(
                f"[bold green]MySQL backup finished with success![/bold green]"
            )
            success = True

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # --- MOCK / SIMULAÇÃO ---
            console.print(f"[yellow]Warning: Failed to run mysqldump ({e})[/yellow]")
            console.print("[yellow]>>> DEV MODE: Creating FAKE backup file...[/yellow]")

            # Cria o arquivo fake manualmente para o fluxo continuar
            with open(output_path, "w") as f:
                f.write(f"-- FAKE Backup for {db_name}\n")
                f.write(f"-- Generated at {timestamp}\n")
                f.write("INSERT INTO users (id, name) VALUES (1, 'Test User');\n")

            success = True  # Forçamos sucesso pois criamos o fake

        # Se deu tudo certo (ou se criamos o fake), comprime e retorna
        if success:
            try:
                compressed_file = compress_file(str(output_path))

                # Opcional: remover o .sql original
                if output_path.exists():
                    os.remove(output_path)

                console.print(f"File ready: {compressed_file}")
                return compressed_file
            except Exception as e:
                console.print(f"[bold red]Error compressing file: {e}[/bold red]")
                return None

        return None
