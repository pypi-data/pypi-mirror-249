"""Response Normalizer."""
from typing import Any, Dict


def response_normalizer(
    nested_dict: Dict[Any, Any], parent_key: str = '', sep: str = '_',
) -> Dict[str, str]:
    """Response Normalizer."""
    flattened_dict = {}
    for key, inner_value in nested_dict.items():
        new_key = (
            '{parent_key}{sep}{key}'.format(parent_key=parent_key, sep=sep, key=key)
            if parent_key
            else key
        )
        if isinstance(inner_value, dict):
            flattened_dict.update(response_normalizer(inner_value, new_key, sep=sep))
        else:
            flattened_dict[new_key] = inner_value
    return flattened_dict
