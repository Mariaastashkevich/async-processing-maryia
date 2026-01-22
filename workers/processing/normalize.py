from pathlib import Path
from typing import Dict, Any

import pandas as pd


def normalize(dataset_path: Path, params: Dict[str, Any]) -> Path:
    """
    :param params: {
          "drop_duplicates": {
            "subset": ["user_id"],
          },
          "fill_nulls": {
            "strategy": "median",
            "columns": ["total_bedrooms", ...]
          },
          "normalize": {
            "columns": ["total_bedrooms", ...],
            "method": "minmax"
          }
        }
    :param dataset_path: "s3//datasets/example_user/example_dataset"
    :return:
    """
    df = pd.read_csv(dataset_path)
    result = df

    drop_cfg = params.get("drop_duplicates")
    if drop_cfg:
        result = result.drop_duplicates(
            subset=drop_cfg.get("subset"),
            keep="first"
        )

    fill_cfg = params.get("fill_nulls")
    if fill_cfg:
        strategy = fill_cfg.get("strategy")
        for column in fill_cfg.get("columns", []):
            match strategy:
                case "median":
                    result[column] = result[column].fillna(result[column].median())
                case "mean":
                    result[column] = result[column].fillna(result[column].mean())
                case "constant":
                    result[column] = result[column].fillna(0)
                case _:
                    raise ValueError(f"Unknown strategy '{strategy}'")

    norm_cfg = params.get("normalize")
    if norm_cfg:
        method = norm_cfg.get("method")
        for column in norm_cfg.get("columns", []):
            match method:
                case "minmax":
                    denom = result[column].max() - result[column].min()
                    if denom != 0:
                        result[column] = (
                                (result[column] - result[column].min()) /
                                (result[column].max() - result[column].min())
                        )
                case "zscore":
                    result[column] = (
                            (result[column] - result[column].mean()) /
                            result[column].std()
                    )
                case _:
                    raise ValueError(f"Unknown method '{method}'")

    output_path = dataset_path.with_name("normalized.csv")
    result.to_csv(output_path, index=False)
    return output_path




