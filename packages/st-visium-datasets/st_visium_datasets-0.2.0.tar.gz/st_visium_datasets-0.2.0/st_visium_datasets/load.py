import logging

import datasets
import tabulate

from st_visium_datasets.utils import sanitize_str, setup_logging
from st_visium_datasets.visium import visium

setup_logging(level="DEBUG")

logger = logging.getLogger(__name__)


def get_visium_dataset_path() -> str:
    """Load visium dataset path for usage with `datasets.load_dataset` from huggingface

    Example:
    >>> from st_visium_datasets import get_visium_dataset_path
    >>> import datasets
    >>> dataset = datasets.load_dataset(get_visium_dataset_path(), name="human-cerebellum")
    >>> builder = datasets.load_dataset_builder(get_visium_dataset_path(), name="human-cerebellum")
    """
    return visium.__file__


def load_visium_dataset_builder(name: str = "all", **kwargs):
    return datasets.load_dataset_builder(
        get_visium_dataset_path(),
        name=sanitize_str(name, sep="-"),
        **kwargs,
    )


def load_visium_dataset(name: str = "all", **kwargs):
    if split := kwargs.get("split"):
        if not split.startswith(visium.VisiumDatasetBuilder.DEFAULT_SPLIT):
            logger.warning(
                f"split '{split}' does not start with '{visium.VisiumDatasetBuilder.DEFAULT_SPLIT}'. "
                f"Only one split is provided: {visium.VisiumDatasetBuilder.DEFAULT_SPLIT}"
            )
            split = visium.VisiumDatasetBuilder.DEFAULT_SPLIT
    else:
        split = visium.VisiumDatasetBuilder.DEFAULT_SPLIT

    kwargs.update({"split": split})
    return datasets.load_dataset(
        get_visium_dataset_path(),
        name=sanitize_str(name, sep="-"),
        **kwargs,
    )


def list_visium_datasets() -> list[str]:
    return list(visium.VisiumDatasetBuilder.builder_configs.keys())


def gen_visium_dataset_stat(name: str = "all") -> dict[str, str | int | float]:
    """TODO: to complete with other interseting stats."""
    config: visium.VisiumDatasetBuilderConfig = (
        visium.VisiumDatasetBuilder.builder_configs[name]
    )
    number_of_spots_under_tissue = sum(
        c.number_of_spots_under_tissue for c in config.visium_configs
    )
    number_of_genes_detected = sum(
        c.number_of_genes_detected for c in config.visium_configs
    )
    return {
        "name": name,
        "number_of_spots_under_tissue": number_of_spots_under_tissue,
        "number_of_genes_detected": number_of_genes_detected,
    }


def gen_visium_dataset_stat_table() -> str:
    names = list_visium_datasets()
    stats = [gen_visium_dataset_stat(name) for name in names]
    return tabulate.tabulate(stats, headers="keys", tablefmt="github")


if __name__ == "__main__":
    table = gen_visium_dataset_stat_table()
    print(table)
