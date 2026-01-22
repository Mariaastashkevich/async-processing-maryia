from pathlib import Path
from typing import Dict, Any

import pandas as pd


def compute_metrics(dataset_path: Path, params: Dict[str, Any]) -> Dict:
    """
    :param dataset_path: "s3//datasets/example_user/example_dataset"
    :param params: {
          "metrics": ["rows", "columns", "null_ratio", "duplicates"],
          "duplicates": {
            "subset": ["user_id"],
            "keep": false
       },
          "limit_rows": 100
    }
    :return: {
        "metrics": {
        "rows": 1,
        "columns": 1,
        "null_ratio": 1,
        "duplicates": 1,
        }
    }
    """
    df = pd.read_csv(dataset_path, nrows=params.get("limit_rows"))
    result = {"metrics": {}}
    metrics = params.get("metrics", [])
    if "rows" in metrics:
        result["metrics"]["rows"] = len(df)
    if "columns" in metrics:
        result["metrics"]["columns"] = len(df.columns)
    if "null_ratio" in metrics:
        result["metrics"]["null_ratio"] = df.isna().mean().mean()
    if "duplicates" in metrics:
        cfg = params.get("duplicates", {})
        result["metrics"]["duplicates"] = int(
            df.duplicated(
            subset=cfg.get("subset"),
            keep=cfg.get("keep", False),
        ).sum()
        )

    return result







