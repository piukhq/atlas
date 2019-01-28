# Atlas

The Atlas project is a stand alone Django Rest API with the purpose of handling and saving subsets of data from Olympus 
to new databases.

## Apps

### Transactions
The transactions app is used to store Merchant transactions (Harvey Nichols) to postgres database and query this db
in a way that allows filtering between two dates. The results of those queries will be sent to blob storage.
##### Endpoints
1. transaction/save - Accepts a payload and saves it to postgres database
2. transaction/blob - Accepts two dates, queries the postgres database for transactions that fall between those dates
and sends the result to Azure blob storage.