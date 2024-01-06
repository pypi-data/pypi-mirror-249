import random

import click


@click.group()
def cli():
    # clear scan results (temp files)
    if random.random() < 0.1:
        from src.scanner import FosslightScanner
        FosslightScanner.clear_scan_results()
