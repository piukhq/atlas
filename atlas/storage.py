import arrow
from azure.common import AzureException
from azure.storage.blob.blockblobservice import BlockBlobService
from azure.storage.blob.models import ContentSettings
from rest_framework.response import Response

from atlas.settings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, logger

bbs = None


def create_blob_from_csv(csv, file_name=None, base_directory=None, container=None):
    global bbs

    if bbs is None:
        bbs = BlockBlobService(
            account_name=AZURE_ACCOUNT_NAME,
            account_key=AZURE_ACCOUNT_KEY)

    date = arrow.utcnow().timestamp
    filename = '{}-{}'.format(file_name, date)
    try:
        bbs.create_blob_from_text(
            container_name=container,
            blob_name='{0}/{1}/{2}.csv'.format(base_directory, file_name, filename),
            content_settings=ContentSettings(content_type='application/CSV'),
            text=csv)

    except AzureException as e:
        if e.error_code == 'ContainerNotFound':
            bbs.create_container(container)
            create_blob_from_csv(csv, file_name, base_directory, container)
        else:
            logger.error('Method: create_blob_from_csv: Azure Exception when saving to blob storage: {}'.format(e))
            raise e

    return Response(data=csv, status=200)
