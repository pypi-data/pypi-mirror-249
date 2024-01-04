from datasets import load_dataset, concatenate_datasets, DatasetDict
from DatasetStructure import DatasetStructure

structurer = DatasetStructure("arubenruben/harem")


for config in ["default", "selective"]:

    primeiro_harem = load_dataset("harem", config)

    mini_harem = DatasetDict({
        'test': primeiro_harem['test']
    })

    primeiro_harem = DatasetDict({
        'train': concatenate_datasets([primeiro_harem['train'], primeiro_harem['validation']])
    })

    structurer.add_dataset_dict(primeiro_harem, f"primeiro_harem_{config}")
    structurer.add_dataset_dict(mini_harem, f"mini_harem_{config}")


second_harem_default = load_dataset("arubenruben/segundo_harem_default")
second_harem_selective = load_dataset("arubenruben/segundo_harem_selective")

structurer.add_dataset_dict(second_harem_default, "segundo_harem_default")
structurer.add_dataset_dict(second_harem_selective, "segundo_harem_selective")

structurer.attach_dataset_card(
    language="pt",
    license="cc-by-4.0",
    annotations_creators=["expert-generated"],
    task_categories=["token-classification"],
    tasks_ids=["named-entity-recognition"],
    pretty_name="HAREM",
    multilinguality='monolingual'
)

structurer.push_to_hub()
