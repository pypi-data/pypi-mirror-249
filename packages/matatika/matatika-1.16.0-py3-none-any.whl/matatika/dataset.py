# pylint: disable=too-many-instance-attributes

"""dataset module"""

from dataclasses import dataclass

from matatika import Resource


@dataclass
class Dataset(Resource):
    """Class for dataset objects"""

    dataset_id: str = None
    alias: str = None
    workspace_id: str = None
    source: str = None
    title: str = None
    description: str = None
    questions: str = None
    raw_data: str = None
    visualisation: str = None
    metadata: str = None
    query: str = None
    version: str = None

    attr_translations = {
        "id": "dataset_id",
        "workspaceId": "workspace_id",
        "rawData": "raw_data",
    }

    @classmethod
    def from_dict(cls, resource_dict: dict):
        dataset, dataset_dict = super().from_dict(resource_dict)

        dataset.dataset_id = dataset_dict.get("dataset_id")
        dataset.alias = dataset_dict.get("alias")
        dataset.workspace_id = dataset_dict.get("workspace_id")
        dataset.source = dataset_dict.get("source")
        dataset.title = dataset_dict.get("title")
        dataset.description = dataset_dict.get("description")
        dataset.questions = dataset_dict.get("questions")
        dataset.raw_data = dataset_dict.get("raw_data")
        dataset.visualisation = dataset_dict.get("visualisation")
        dataset.metadata = dataset_dict.get("metadata")
        dataset.query = dataset_dict.get("query")

        return dataset


@dataclass
class DatasetV0_1(Dataset):  # pylint: disable=invalid-name
    """Class for dataset resource version 0.1"""

    version: str = "datasets/v0.1"


@dataclass
class DatasetV0_2(Dataset):  # pylint: disable=invalid-name
    """Class for dataset resource version 0.2"""

    version: str = "datasets/v0.2"
