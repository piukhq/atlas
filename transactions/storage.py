import arrow
from azure.common import AzureException
from azure.storage.blob.blockblobservice import BlockBlobService
from azure.storage.blob.models import ContentSettings
from rest_framework.response import Response
from atlas.settings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, AZURE_CONTAINER, AZURE_TRANSACTION_BASE_DIRECTORY,\
    logger

bbs = None


def create_blob_from_json(json, scheme_slug):
    global bbs

    if bbs is None:
        bbs = BlockBlobService(
            account_name=AZURE_ACCOUNT_NAME,
            account_key=AZURE_ACCOUNT_KEY)

    date = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss.SSSSS')
    filename = '{}-{}'.format(scheme_slug, date)
    try:
        bbs.create_blob_from_text(
            container_name=AZURE_CONTAINER,
            blob_name='{0}/{1}/{2}.json'.format(AZURE_TRANSACTION_BASE_DIRECTORY, scheme_slug, filename),
            content_settings=ContentSettings(content_type='application/json'),
            text=json)

    except AzureException as e:
        if e.error_code == 'ContainerNotFound':
            bbs.create_container(AZURE_CONTAINER)
            create_blob_from_json(json, scheme_slug)
        else:
            logger.error('Azure Exception when saving to blob storage: {}'.format(e))
            raise e

    return Response(data=json, status=200)
