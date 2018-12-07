import arrow
from azure.storage.blob.blockblobservice import BlockBlobService
from azure.storage.blob.models import ContentSettings

from atlas.settings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, AZURE_CONTAINER, AZURE_TRANSACTION_BASE_DIRECTORY

bbs = None


def create_blob_from_json(json):
    global bbs

    if bbs is None:
        bbs = BlockBlobService(
            account_name=AZURE_ACCOUNT_NAME,
            account_key=AZURE_ACCOUNT_KEY)

    date = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss.SSSSS')
    filename = '{}-{}'.format("Harvey Nichols Transactions", date)
    bbs.create_blob_from_text(
        container_name=AZURE_CONTAINER,
        blob_name='{0}/{1}/{2}.json'.format(AZURE_TRANSACTION_BASE_DIRECTORY, "Harvey Nichols Transactions", filename),
        content_settings=ContentSettings(content_type='application/json'),
        text=json)
