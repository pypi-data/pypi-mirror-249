# pylint: disable=too-many-locals

"""Parse Service"""

import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

import yaml
from nbconvert import MarkdownExporter
from traitlets.config import Config

from matatika import Resource
from matatika.channel import Channel
from matatika.dataset import Dataset

NOTEBOOK = [".ipynb"]
YAML = [".yml", ".yaml"]
SUPPORTED_FILETYPES = NOTEBOOK + YAML


def parse_resources(user_file: Path):
    """Parse resources from files"""
    resources: List[Resource] = []

    if user_file.is_dir():
        for file in user_file.iterdir():
            resources.extend(parse_resources(file))

        return resources

    if user_file.suffix in NOTEBOOK:
        resources.append(_parse_dataset_from_notebook(user_file))
    elif user_file.suffix in YAML:
        resources.extend(_parse_resources_from_yaml(user_file))

    return resources


def _parse_resources_from_yaml(yaml_file: Path):
    resources: List[Resource] = []

    with yaml_file.open() as file:
        yaml_dict: dict = yaml.safe_load(file)
        version: str = yaml_dict.get("version")

        if version == "datasets/v0.2":
            dataset = Dataset.from_dict(yaml_dict)
            dataset.alias = dataset.alias or yaml_file.name
            resources.append(dataset)

        elif version == "channels/v0.1":
            channel = Channel.from_dict(yaml_dict)
            channel.name = channel.name or yaml_file.name
            resources.append(channel)

        else:
            datasets_dict: dict = yaml_dict["datasets"]

            for alias, dataset_dict in datasets_dict.items():
                dataset = Dataset.from_dict(dataset_dict)
                dataset.alias = dataset.alias or alias
                resources.append(dataset)

    return resources


def _parse_dataset_from_notebook(file: Path):
    config = Config()
    config.TemplateExporter.exclude_output_prompt = True
    config.TemplateExporter.exclude_input = True
    config.TemplateExporter.exclude_input_prompt = True
    config.ExtractOutputPreprocessor.enabled = False

    md_exporter = MarkdownExporter(config=config)
    md_str = md_exporter.from_file(file)[0]

    match = re.search(r"#+\s(.+)", md_str)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return Dataset.from_dict(
        {
            "id": str(uuid.uuid4()),
            "title": match.group(1) if match else f"Generated Report ({timestamp})",
            "description": md_str,
            "alias": file.name,
        }
    )
