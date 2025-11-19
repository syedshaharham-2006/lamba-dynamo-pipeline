import csv
import io
import boto3
from decimal import Decimal  # Import Decimal

# Initialize S3 and DynamoDB clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Configuration
BUCKET_NAME = 'cde-dynamo'
DYNAMO_TABLE_NAME = 'stockData'

# DynamoDB Table reference
table = dynamodb.Table(DYNAMO_TABLE_NAME)

# Define the stock symbols
STOCK_SYMBOLS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "FB", "TSLA", "NFLX", "NVDA", "BABA", "INTC",
    "CSCO", "ADBE", "ORCL", "IBM", "PYPL", "CRM", "QCOM", "AMD", "TXN", "AVGO",
    "COST", "SHOP", "SPOT", "UBER", "LYFT", "SQ", "TWTR", "SNAP", "DOCU", "ZM",
    "ROKU", "EA", "ATVI", "MRNA", "PFE", "JNJ", "KO", "PEP", "DIS", "V", "MA",
    "GS", "JPM", "BAC", "WMT", "TGT", "HD", "CVX", "XOM", "NKE", "MCD"
]

def save_csv_to_dynamodb(symbol):
    # Read the CSV file from S3
    response = s3.get_object(Bucket=BUCKET_NAME, Key=f"stocks/{symbol}.csv")
    csv_data = response['Body'].read().decode('utf-8')
    
    # Parse the CSV data
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    
    # Prepare data for DynamoDB and insert
    for row in csv_reader:
        date = row['date']
        open_price = row['open']
        close_price = row['close']
        high_price = row['high']
        low_price = row['low']
        volume = row['volume']
        
        # Convert to Decimal to be compatible with DynamoDB
        table.put_item(
            Item={
                'symbol': symbol,
                'date': date,
                'open': Decimal(open_price),
                'close': Decimal(close_price),
                'high': Decimal(high_price),
                'low': Decimal(low_price),
                'volume': Decimal(volume)
            }
        )
        print(f"Inserted {symbol} data for {date} into DynamoDB")

def lambda_handler(event, context):
    # Iterate over all stock symbols
    for symbol in STOCK_SYMBOLS:
        save_csv_to_dynamodb(symbol)
    
    return {
        "statusCode": 200,
        "body": f"Successfully uploaded stock data from CSVs in S3 to DynamoDB."
    }
