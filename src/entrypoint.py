import enum
import logging
import json
import os


REPOSITORY = os.environ["GITHUB_REPOSITORY"]
SHA = os.environ["GITHUB_SHA"]
EVENT = os.environ["GITHUB_EVENT_NAME"]
EVENT_PATH = os.environ["GITHUB_EVENT_PATH"]
TOKEN = os.environ["INPUT_GITHUBTOKEN"]
MAJOR_LIST = os.environ["INPUT_MAJOR"].split(',')
MINOR_LIST = os.environ["INPUT_MINOR"].split(',')
PATCH_LIST = os.environ["INPUT_PATCH"].split(',')
DEFAULT_PART = os.environ["INPUT_DEFAULTPART"].upper()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Parts(enum.Enum):
    MAJOR = 2
    MINOR = 1
    PATCH = 0
    NULL = -1


class LabelMap(dict):
    def add_labels(self, label_list, part):
        for label in label_list:
            if label:
                self[label] = part


def build_label_map():
    label_map = LabelMap()

    label_map.add_labels(MAJOR_LIST, Parts.MAJOR)
    label_map.add_labels(MINOR_LIST, Parts.MINOR)
    label_map.add_labels(PATCH_LIST, Parts.PATCH)
    return label_map


LABELMAP = build_label_map()


def main():
    with open(EVENT_PATH, 'r') as fh:
        payload = json.load(fh)

    labels = payload['pull_request']['labels']
    part = Parts.__members__[DEFAULT_PART]

    for label in labels:
        label_part = LABELMAP.get(label["name"])
        if label_part is None:
            continue

        if label_part.value > part.value:
            part = label_part

    print(f"::set-output name=part::{part.name.lower()}")


if __name__ == "__main__":
    main()
