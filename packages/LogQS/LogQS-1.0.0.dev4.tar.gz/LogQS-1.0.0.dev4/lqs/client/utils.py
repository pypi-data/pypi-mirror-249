import io
import os
import base64
from pathlib import Path
from typing import TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor

import requests

try:
    # TODO: better way to handle this?
    # doesn't seem like it should be a hard dependency
    from PIL import Image as PILImage
except ImportError:
    PILImage = None

from lqs.interface.core.models import Record

if TYPE_CHECKING:
    from lqs.client import RESTClient


class Utils:
    def __init__(self, app: "RESTClient"):
        self.app = app

    def upload_log_object(
        self,
        log_id: str,
        file_path: str,
        object_key: str = None,
        part_size: int = 100 * 1024 * 1024,
        max_workers: int | None = 8,
    ):
        if object_key is None:
            object_key = file_path.split("/")[-1]

        log_object = self.app.create.log_object(
            log_id=log_id,
            key=object_key,
        ).data

        object_size = os.path.getsize(file_path)
        number_of_parts = object_size // part_size + 1
        log_object_parts = []
        if max_workers is not None:
            futures = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                for idx in range(0, number_of_parts):
                    offset = idx * part_size
                    with open(file_path, "rb") as f:
                        f.seek(offset)
                        data = f.read(part_size)
                        futures.append(
                            executor.submit(
                                self.upload_log_object_part,
                                log_id=log_id,
                                object_key=object_key,
                                size=len(data),
                                part_number=idx + 1,
                                data=data,
                            )
                        )

                for future in futures:
                    log_object_parts.append(future.result())
        else:
            for idx in range(0, number_of_parts):
                offset = idx * part_size
                with open(file_path, "rb") as f:
                    f.seek(offset)
                    data = f.read(part_size)
                    log_object_parts.append(
                        self.upload_log_object_part(
                            log_id=log_id,
                            object_key=object_key,
                            size=len(data),
                            part_number=idx + 1,
                            data=data,
                        )
                    )

        log_object = self.app.update.log_object(
            log_id=log_id, object_key=object_key, data={"upload_state": "complete"}
        ).data

        return log_object, log_object_parts

    def upload_log_objects(
        self,
        log_id: str,
        file_dir: str,
        key_replacement: tuple[str, str] = None,
        key_prefix: str = None,
        part_size: int = 100 * 1024 * 1024,
        max_workers: int | None = 8,
        fail_if_empty: bool = True,
    ):
        upload_result_sets = []
        for file_path in Path(file_dir).rglob("*"):
            if os.path.isfile(file_path):
                object_key = str(file_path)
                if key_replacement is not None:
                    object_key = object_key.replace(*key_replacement)
                if key_prefix is not None:
                    object_key = os.path.join(key_prefix, object_key)
                if object_key.startswith("/"):
                    object_key = object_key[1:]
                upload_result = self.upload_log_object(
                    log_id=log_id,
                    file_path=file_path,
                    object_key=object_key,
                    part_size=part_size,
                    max_workers=max_workers,
                )
                upload_result_sets.append(upload_result)
        if fail_if_empty and len(upload_result_sets) == 0:
            raise Exception(f"No files found in {file_dir}")
        return upload_result_sets

    def upload_log_object_part(self, log_id, object_key, size, part_number, data):
        object_part = self.app.create.log_object_part(
            log_id=log_id,
            object_key=object_key,
            size=size,
            part_number=part_number,
        ).data

        upload_object_data_url = object_part.presigned_url
        response = requests.put(
            upload_object_data_url,
            data=data,
        )

        if response.status_code != 200:
            raise Exception(f"Error while uploading object part: {response.text}")

        return self.app.fetch.log_object_part(
            log_id=log_id,
            object_key=object_key,
            part_number=part_number,
        ).data

    def load_auxiliary_data_image(self, record: Record):
        if record.auxiliary_data is None:
            return None
        if "image" not in record.auxiliary_data:
            return None
        if PILImage is None:
            raise Exception("PIL is not installed")
        encoded_webp_data = record.auxiliary_data["image"]
        decoded_webp_data = base64.b64decode(encoded_webp_data)
        image = PILImage.open(io.BytesIO(decoded_webp_data))
        return image
