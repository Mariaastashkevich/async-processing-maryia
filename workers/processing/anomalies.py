from pathlib import Path
from typing import Dict, Any

import pandas as pd
from scipy import stats


def detect_anomalies(dataset_path: Path, params: Dict[str, Any]) -> Dict:
    """
    :param dataset_path:  "s3//datasets/example_user/example_dataset"
    :param params: {
            "column": "total_rooms",
            "strategy": "zscore" or "IQR"
            "limit_rows: 1000",

    }
    :return: {
        "anomalies_count": 12
        "anomalies": [3545667755, 67778889999, ...],
    }
    """

    df = pd.read_csv(dataset_path, nrows=params.get("limit_rows"))
    column = params.get("column")

    if not column:
        raise ValueError(f"'column' param is required")
    if column not in df.columns:
        raise ValueError(f"'column' doesn't exist in dataset")

    series = df[column].dropna()
    strategy = params.get("strategy")

    match strategy:
        case "zscore":
            z_scores = stats.zscore(series)
            mask = (z_scores > 3) | (z_scores < -3)
            anomalies = series[mask].tolist()
        case "IQR":
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)

            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            anomalies = series[(series > upper_bound) | (series < lower_bound)].tolist()
        case _:
            raise ValueError(f"Unknown strategy '{strategy}'")

    return {
        "anomalies_count": len(anomalies),
        "anomalies": anomalies,
    }


