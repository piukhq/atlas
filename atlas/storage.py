import arrow
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
from rest_framework.response import Response

from atlas.settings import BLOB_STORAGE_DSN, logger

bbs = None


def create_blob_from_csv(csv, file_name=None, base_directory=None, container=None):
    global bbs

    if bbs is None:
        bbs = BlobServiceClient.from_connection_string(BLOB_STORAGE_DSN)

    date = arrow.utcnow().timestamp
    filename = '{}-{}'.format(file_name, date)

    try:
        blob_client = bbs.get_blob_client(container=container, blob=filename)
        blob_client.upload_blob(csv)
    except ResourceNotFoundError as e:
        if e.error_code.value == 'ContainerNotFound':
            bbs.create_container(container)
            create_blob_from_csv(csv, file_name, base_directory, container)
        else:
            logger.error('Method: create_blob_from_csv: Azure Exception when saving to blob storage: {}'.format(e))
            raise e

    return Response(data=csv, status=200)
