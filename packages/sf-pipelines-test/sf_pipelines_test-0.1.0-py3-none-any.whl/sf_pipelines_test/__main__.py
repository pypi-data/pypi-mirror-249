import click as click

from sf_pipelines_test.annex_a_pipeline.cli import annex_a
from sf_pipelines_test.datasets.cin_census.cin_cli import cin_census
from sf_pipelines_test.datasets.social_work_workforce.csww_cli import csww
from sf_pipelines_test.ssda903_pipeline.cli import s903


@click.group()
def cli():
    pass


cli.add_command(annex_a)
cli.add_command(cin_census)
cli.add_command(s903)
cli.add_command(csww)

if __name__ == "__main__":
    cli()
