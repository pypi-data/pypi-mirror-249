import logging
from pathlib import Path

import pandas as pd

THIS_DIR = Path(__file__).parent
OLIST_CUSTOMERS_DATASET_FPATH = THIS_DIR / "olist_customers_dataset.csv"

class IngestData:
    """
    Classe d'ingestion de données qui ingère les données de la source et renvoie un DataFrame.
    """

    def __init__(self) -> None:
        """Initialiser la classe d'ingestion de données."""
        pass

    def get_data(self) -> pd.DataFrame:
        df = pd.read_csv(OLIST_CUSTOMERS_DATASET_FPATH)
        return df



def ingest_data() -> pd.DataFrame:
    """
    Args:
        None
    Returns:
        df: pd.DataFrame
    """
    try:
        ingest_data = IngestData()
        df = ingest_data.get_data()
        return df
    except Exception as e:
        logging.error(e)
        raise e
