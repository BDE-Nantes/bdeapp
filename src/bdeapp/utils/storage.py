import uuid
from pathlib import Path


def uuid_path(instance, filename: str, suffix: str = "", from_instance: bool = False):
    if from_instance and hasattr(instance, "uuid"):
        path_uuid = instance.uuid
    else:
        path_uuid = uuid.uuid4()

    extension = Path(filename).suffix.lower()
    return f"{suffix}{path_uuid}{extension}"
