import os

import boto3
from botocore.exceptions import ClientError
from rich.console import Console

from .base import StorageStrategy

console = Console()


class S3Storage(StorageStrategy):
    def __init__(self, bucket_name, region, access_key, secret_key):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def save(self, source_path: str, destination_filename: str) -> None:
        console.print(f"[cyan]Uploading to AWS S3 ({self.bucket_name})...[/cyan]")

        try:
            self.client.upload_file(source_path, self.bucket_name, destination_filename)
            console.print(
                f"[bold green]Upload success! File: s3://{self.bucket_name}/{destination_filename}[/bold green]"
            )

            os.remove(source_path)
            console.print("[dim]Local temporary file removed.[/dim]")

        except ClientError as e:
            console.print(f"[bold red]AWS S3 Erro:[/bold red] {e}")
            console.print("Check your credentials and bucket name in config.yaml")
        except Exception as e:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")
