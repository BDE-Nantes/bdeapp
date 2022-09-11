import fnmatch
from typing import Container

from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

import magic


@deconstructible
class ImageSizeValidator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def __call__(self, image: ImageFieldFile) -> None:
        if image.width != self.width or image.height != self.height:
            raise ValidationError(
                _("Image must have a width of %(width)s and a height of %(height)s"),
                params={"height": self.height, "width": self.width},
            )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.width == other.width
            and self.height == other.height
        )


@deconstructible
class FileValidator(object):
    error_messages = {
        "max_size": _(
            "Ensure this file size is not greater than %(max_size)s. Your file size is %(size)s."
        ),
        "min_size": _(
            "Ensure this file size is not less than %(min_size)s. Your file size is %(size)s."
        ),
        "content_type": _("Files of type %(content_type)s are not supported."),
    }

    def __init__(
        self, max_size: int | None = None, min_size: int | None = None, content_types=()
    ):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            raise ValidationError(
                self.error_messages["max_size"],
                code="max_size",
                params={
                    "max_size": filesizeformat(self.max_size),
                    "size": filesizeformat(data.size),
                },
            )

        if self.min_size is not None and data.size < self.min_size:
            raise ValidationError(
                self.error_messages["min_size"],
                code="min_size",
                params={
                    "min_size": filesizeformat(self.min_size),
                    "size": filesizeformat(data.size),
                },
            )

        if self.content_types:
            file_content_type = magic.from_buffer(data.read(2048), mime=True)
            data.seek(0)

            match = any(
                fnmatch.fnmatch(file_content_type.lower(), content_type.lower())
                for content_type in self.content_types
            )

            if not match:
                raise ValidationError(
                    self.error_messages["content_type"],
                    code="content_type",
                    params={"content_type": file_content_type},
                )

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator)
            and self.max_size == other.max_size
            and self.min_size == other.min_size
            and self.content_types == other.content_types
        )