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

    for field, filedata in form.files.items():
        generated_uuid = uuid.uuid4()
        secret_hash = hashlib.sha1(force_bytes(generated_uuid)).hexdigest()
        valid_file_name = file_storage.get_valid_name(filedata.name)
        root, ext = os.path.splitext(valid_file_name)
        full_path = os.path.join(
            settings.DJANGOCMS_FORMS_FILE_STORAGE_DIR,
            form.form_definition.upload_to,
            '%s_%s%s' % (root, secret_hash, ext)
        )
        filename = file_storage.get_available_name(full_path)
        file_storage.save(filename, filedata)
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
