from datasets import DatasetDict, Dataset
from huggingface_hub import DatasetCard


class DatasetStructure:
    def __init__(self, repo_name: str) -> None:
        """
        Initializes a new instance of the DatasetStructure class.

        Args:
            repo_name (str): The name of the repository.

        Returns:
            None
        """
        self.repo_name = repo_name
        self.dataset_dicts = []
        self.config_names = []
        self.dataset_card = None

    def add_dataset_dict(self, dataset_dict: DatasetDict, config_name: str) -> None:
        """
        Adds a dataset dictionary to the dataset structure.

        Args:
            dataset_dict (DatasetDict): The dataset dictionary to add.
            config_name (str): The name of the configuration.

        Returns:
            None

        Raises:
            ValueError: If the config_name already exists in the dataset structure.
        """
        if config_name in self.config_names:
            raise ValueError(f"config_name {config_name} already exists in {self.repo_name}")

        self.dataset_dicts.append(dataset_dict)
        self.config_names.append(config_name)

    def add_dataset(self, dataset: Dataset, config_name: str, split: str = "train") -> None:
        """
        Adds a dataset to the dataset structure.

        Args:
            dataset (Dataset): The dataset to add.
            config_name (str): The name of the configuration.
            split (str, optional): The split of the dataset. Defaults to "train".

        Returns:
            None
        """
        self.add_dataset_dict(DatasetDict({split: dataset}), config_name)

    def attach_dataset_card(self, language: str,
                            license: str,
                            annotations_creators: str,
                            task_categories: str,
                            tasks_ids: str,
                            pretty_name: str,
                            multilinguality: str = 'monolingual'):
        """
        Attaches a dataset card to the dataset structure.

        Args:
            language (str): The language of the dataset.
            license (str): The license of the dataset.
            annotations_creators (str): The creators of the annotations.
            task_categories (str): The categories of the task.
            tasks_ids (str): The IDs of the tasks.
            pretty_name (str): The pretty name of the dataset.
            multilinguality (str, optional): The multilinguality of the dataset. Defaults to 'monolingual'.

        Returns:
            None

        Raises:
            ValueError: If no dataset card is found.
        """
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
        """
        Pushes the dataset structure and dataset card to the Hugging Face Hub.

        Args:
            private (bool, optional): Whether to push the dataset structure as private. Defaults to False.

        Returns:
            None
        """
        for dataset_dict, config_name in zip(self.dataset_dicts, self.config_names):
            dataset_dict.push_to_hub(
                self.repo_name, config_name=config_name, set_default=False, private=private)

        if self.dataset_card:
            print("Pushing dataset card...")
            self.dataset_card.push_to_hub(self.repo_name)
        else:
            print("No dataset card to push.")
