# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib
import os
import uuid

from django.core.files.base import File
from django.core.files.storage import get_storage_class
from django.db.models.fields.files import FieldFile
from django.utils.encoding import force_bytes
from django.utils.functional import LazyObject

from .conf import settings


class FileStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.DJANGOCMS_FORMS_FILE_STORAGE)()

file_storage = FileStorage()


def handle_uploaded_files(form):
    if len(form.file_fields):
        for field in form.file_fields:
            uploaded_file = form.cleaned_data.get(field, None)
            if uploaded_file is None:
                continue

            valid_file_name = file_storage.get_valid_name(uploaded_file.name)
            root, ext = os.path.splitext(valid_file_name)
            secret_hash = hashlib.sha1(force_bytes(uuid.uuid4())).hexdigest()
            filename = file_storage.get_available_name(os.path.join(
                settings.DJANGOCMS_FORMS_FILE_STORAGE_DIR,
                form.form_definition.upload_to,
                '{root}_{hash}{ext}'.format(root=root, hash=secret_hash, ext=ext)))
            file_storage.save(filename, uploaded_file)
            form.cleaned_data[field] = StoredUploadedFile(filename)


class StoredUploadedFile(FieldFile):
    """
    A wrapper for uploaded files that is compatible to the FieldFile class, i.e.
    you can use instances of this class in templates just like you use the value
    of FileFields (e.g. `{{ my_file.url }}`)
    """

    def __init__(self, name):
        File.__init__(self, None, name)
        self.field = self

    @property
    def storage(self):
        return file_storage

    def save(self, *args, **kwargs):
        raise NotImplementedError('Static files are read-only')

    def delete(self, *args, **kwargs):
        raise NotImplementedError('Static files are read-only')

    def __unicode__(self):
        return self.name
