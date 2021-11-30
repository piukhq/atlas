import datetime
import logging

from azure.core.exceptions import ResourceNotFoundError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atlas.csv_writer import write_to_csv
from atlas.decorators import token_check
from atlas.settings import TRANSACTION_REPORTS_CONTAINER
from atlas.storage import create_blob_from_csv
from prometheus.signals import transaction_fail, transaction_success
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer

logger = logging.getLogger(__name__)


class TransactionBlobView(APIView):
    """View to query Transaction database and save result to blob storage"""

    @staticmethod
    @token_check
    def post(request):
        start = request.data["start"]
        end = request.data["end"]
        scheme_slug = request.data["scheme_slug"]

        if start < end:

            try:  # Get transactions in a list of dicts so we can write them to csv
                transactions = get_transactions(start, end, scheme_slug)
            except (ValueError, TypeError) as e:
                logger.exception(
                    "Method: TransactionBlobView.get_transactions: Date must reflect YYYY-MM-DD format: {}".format(e)
                )
                return Response(
                    data="Date must reflect YYYY-MM-DD format: {}".format(e), status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(data="Date Error: start date must precede end date", status=status.HTTP_400_BAD_REQUEST)

        try:
            transactions_csv = write_to_csv(transactions)
        except IndexError:
            logger.info(
                "Method: TransactionBlobView.write_to_csv: No transactions between these dates: {}--{}".format(
                    start, end
                )
            )
            return Response(
                data="No transactions exist between these dates: {}--{}".format(start, end),
                status=status.HTTP_204_NO_CONTENT,
            )

        try:
            create_blob_from_csv(
                transactions_csv,
                file_name=scheme_slug,
                base_directory="schemes",
                container=TRANSACTION_REPORTS_CONTAINER,
            )

        except ResourceNotFoundError as e:
            logger.exception(
                "Method: TransactionBlobView.create_blob_from_csv: Error saving to Blob storage - {} data - {}".format(
                    e, transactions
                )
            )
            return Response(
                data="Error saving to blob storage - {} data - {}".format(e, transactions), status=e.status_code
            )

        except Exception as e:
            logger.exception(
                "Method: TransactionBlobView.create_blob_from_csv: Error saving to Blob storage - {} data - {}".format(
                    e, transactions
                )
            )
            return Response(
                data="Error saving to blob storage - {} data - {}".format(e, transactions),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=transactions, status=status.HTTP_200_OK)


class TransactionSaveView(APIView):
    """View to handle incoming transaction data from Aphrodite and save to postgres"""

    @staticmethod
    @token_check
    def post(request):
        transaction_serializer = TransactionSerializer(data=request.data)

        if transaction_serializer.is_valid():
            transaction_serializer.save()
            transaction_success.send(sender="TransactionSaveView.post")
            return Response(
                data="Transaction saved: {}".format(transaction_serializer.data), status=status.HTTP_201_CREATED
            )

        logger.warning("TransactionSaveView.post: Transaction NOT saved {}".format(transaction_serializer.errors))
        transaction_fail.send(sender="TransactionSaveView.post")

        id_error = transaction_serializer.errors.get("transaction_id")
        if id_error and id_error[0].code == "unique":
            return Response(
                data="Duplicate transaction ignored: {}".format(transaction_serializer.data), status=status.HTTP_200_OK
            )

        return Response(
            data="Transaction NOT saved: {}".format(transaction_serializer.errors), status=status.HTTP_400_BAD_REQUEST
        )


def get_transactions(start_date, end_date, slug):
    format_str = "%Y-%m-%d"
    start_datetime = datetime.datetime.strptime(start_date, format_str)
    end_datetime = datetime.datetime.strptime(end_date, format_str) + datetime.timedelta(days=1)

    transactions = Transaction.objects.filter(created_date__range=(start_datetime, end_datetime), scheme_provider=slug)
    list_for_csv = list()

    for transaction in transactions:
        list_for_csv.append(
            {
                "created_date": transaction.created_date,
                "scheme_provider": transaction.scheme_provider,
                "response": transaction.response,
                "transaction_id": transaction.transaction_id,
                "status": transaction.status,
                "transaction_date": transaction.transaction_date,
                "user_id": transaction.user_id,
                "amount": transaction.amount,
            }
        )

    return list_for_csv
