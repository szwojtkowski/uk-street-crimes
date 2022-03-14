import logging

import click

from uk.street.crimes.domain.pipeline import StreetCrimeExtractionPipeline
from uk.street.crimes.external.parsers import (
    StreetCrimeOutcomeParser,
    StreetCrimeParser,
)
from uk.street.crimes.external.providers import (
    StreetCrimeCsvProvider,
    StreetCrimeOutcomeCsvProvider,
    get_csv_data_subdir_paths,
)
from uk.street.crimes.external.repositories import StreetCrimeElasticsearchRepository


@click.command()
@click.argument("data_dir", type=click.STRING)
@click.option(
    "--elasticsearch-host", type=click.STRING, default="http://localhost:9200"
)
@click.option(
    "--log_level", type=click.STRING, default=logging.getLevelName(logging.WARNING)
)
def extract_street_crime_data(data_dir, elasticsearch_host, log_level):
    logging.basicConfig(level=log_level)
    logging.info("Running extract_street_crime_data command.")

    street_crime_repository = StreetCrimeElasticsearchRepository(elasticsearch_host)

    for directory in get_csv_data_subdir_paths(data_dir):
        logging.info(f"Processing {directory}")
        street_crime_provider = StreetCrimeCsvProvider(
            data_dir=directory, street_crime_parser=StreetCrimeParser()
        )
        street_crime_outcome_provider = StreetCrimeOutcomeCsvProvider(
            data_dir=directory, street_crime_outcome_parser=StreetCrimeOutcomeParser()
        )

        street_crime_extraction_pipeline = StreetCrimeExtractionPipeline(
            street_crime_provider,
            street_crime_outcome_provider,
            street_crime_repository,
        )

        street_crime_extraction_pipeline.run()
