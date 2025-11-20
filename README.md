# AWS Stock Data Pipeline
> **Automated, Serverless Stock Data ETL:**  
> End-to-end daily stock data pipeline using Amazon EventBridge, Lambda, S3, SQS, and DynamoDB.

## 🚀 Architecture Overview

This pipeline automatically generates synthetic stock data daily, stores it securely, manages file notifications, processes uploaded CSVs, and loads final structured data into DynamoDB — all using AWS serverless features.

**Pipeline Steps:**
1. **Amazon EventBridge**   
   - Scheduled rule triggers data generation Lambda daily.

2. **Lambda #1 — Data Generation**  
   - Generates random 30 days OHLCV for 50 symbols.
   - Saves each as `stocks/{symbol}.csv` in S3.

3. **Amazon S3 — Data Storage** 
   - Stores CSV files.
   - Each upload triggers an SQS message.

4. **Amazon SQS — Notification Queue** 
   - Receives notifications for new S3 files.
   - Acts as buffer between S3 and next Lambda.

5. **Lambda #2 — CSV Processor**
   - Triggered by SQS.
   - Reads S3 CSV, parses records.
   - Inserts each row into DynamoDB.

6. **Amazon DynamoDB — Final Storage** 
   - Table: `stockData`
   - Keys: `symbol` (PK), `date` (SK)
   - Stores OHLCV, volume.

---

## 📊 Data Flow

flowchart TD
A[EventBridge: Scheduled Rule] --> B[Lambda #1: Generate Data]
B --> C[S3: Store CSVs]
C --> D[SQS: Notification]
D --> E[Lambda #2: Process CSV]
E --> F[DynamoDB: Insert Data]

---

**Step-by-step:**
- EventBridge → Lambda #1 → S3
- S3 upload → SQS message
- SQS → Lambda #2 → S3 (read) → DynamoDB (write)

---

## 🗂️ Repository Structure

```
project-root
│
├── lambda_generate/ # Lambda #1: Generate & Upload CSV
│ └── lambda_function.py
├── lambda_process/ # Lambda #2: S3 → DynamoDB
│ └── lambda_function.py
└── README.md

```

---

## λ Lambda #1 — Generate CSV (Summary)

- Loops 50 symbols, 30 days each
- Generates OHLCV data
- Uploads `stocks/{symbol}.csv` to S3
- **IAM Needed:** `s3:PutObject`

---

## ⚙️ Lambda #2 — CSV Loader (Summary)

- Triggered by SQS (not S3)
- Reads uploaded CSV from S3
- Converts numerics to `Decimal`
- Writes each record to DynamoDB
- **IAM Needed:**  
  - `s3:GetObject`
  - `dynamodb:PutItem`
  - `sqs:ReceiveMessage`

---

## 🔧 Deployment: IAM and AWS Resources

- **IAM Roles must allow:**
    - `s3:PutObject`
    - `s3:GetObject`
    - `dynamodb:PutItem`
    - `sqs:ReceiveMessage`
    - `logs:*`
- **AWS Services used:**
    - EventBridge Scheduler
    - 2× Lambda Functions
    - S3 Bucket (for CSVs)
    - SQS Queue
    - DynamoDB Table

---

##  Dependencies

- **AWS Lambda Core:**  
  - `boto3`
  - `csv`
  - `decimal`
- No external libraries required.

---

## 📊 DynamoDB Table Schema

| Attribute | Type   | Role             | Description        |
|-----------|--------|------------------|--------------------|
| symbol    | String | Partition Key    | Stock symbol       |
| date      | String | Sort Key         | `YYYY-MM-DD` date  |
| open      | Number | -                | Opening price      |
| close     | Number | -                | Closing price      |
| high      | Number | -                | Highest price      |
| low       | Number | -                | Lowest price       |
| volume    | Number | -                | Trade volume       |

---

## 📖 Example Usage

- Deploy using the AWS Console or Infrastructure-as-Code (CloudFormation, CDK, SAM).
- Ensure IAM roles grant Lambda functions correct permissions.
- Set the EventBridge rule for daily triggers (e.g., midnight UTC).
- View processed data in the DynamoDB table `stockData`.

---

