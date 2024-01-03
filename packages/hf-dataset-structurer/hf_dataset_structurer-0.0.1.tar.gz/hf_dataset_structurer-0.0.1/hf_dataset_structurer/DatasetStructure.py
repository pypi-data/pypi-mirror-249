from datasets import DatasetDict, Dataset
from huggingface_hub import DatasetCard


class DatasetStructure:
    def __init__(self, repo_name: str) -> None:
        self.repo_name = repo_name
        self.dataset_dicts = []
        self.config_names = []
        self.dataset_card = None

    def add_dataset_dict(self, dataset_dict: DatasetDict, config_name: str) -> None:
        if config_name in self.config_names:
            raise ValueError(f"config_name {config_name} already exists in {
                             self.repo_name}")

        self.dataset_dicts.append(dataset_dict)
        self.config_names.append(config_name)

    def add_dataset(self, dataset: Dataset, config_name: str, split: str = "train") -> None:
        self.add_dataset_dict(DatasetDict({split: dataset}), config_name)

    def attach_dataset_card(self, language, license, annotations_creators, task_categories, tasks_ids, pretty_name, multilinguality='monolingual'):
        self.dataset_card = DatasetCard.load(self.repo_name)

        if self.dataset_card is None:
            raise ValueError("No dataset card found. Please create one first.")

        self.dataset_card.language = language
        self.dataset_card.license = license
        self.dataset_card.annotations_creators = annotations_creators
        self.dataset_card.task_categories = task_categories
        self.dataset_card.tasks_ids = tasks_ids
        self.dataset_card.multilinguality = multilinguality
        self.dataset_card.pretty_name = pretty_name
        self.dataset_card.repo_type = "dataset"

    def push_to_hub(self, private: bool = False) -> None:

        for dataset_dict, config_name in zip(self.dataset_dicts, self.config_names):
            dataset_dict.push_to_hub(
                self.repo_name, config_name=config_name, set_default=False, private=private)

        if self.dataset_card:
            print("Pushing dataset card...")
            self.dataset_card.push_to_hub(self.repo_name)
        else:
            print("No dataset card to push.")