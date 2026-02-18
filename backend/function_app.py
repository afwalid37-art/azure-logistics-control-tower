import azure.functions as func
import logging
import pandas as pd
import sqlalchemy
import os
import io

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", 
                  path="uploads/{name}", 
                  connection="AzureWebJobsStorage")
def blob_trigger(myblob: func.InputStream):
    # 1. Setup Database Bridge
    connection_string = os.getenv("SqlConnectionString")
    engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")
    
    logging.info(f"Watchdog detected new file: {myblob.name}")

    # 2. Read the blob data FIRST
    blob_bytes = myblob.read()
    if myblob.name.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(blob_bytes))
    else:
        df = pd.read_excel(io.BytesIO(blob_bytes))

    # 3. Validation Gatekeeper (Safety First!)
    required_columns = [
        "Order_ID", "Order_Date", "City", "Product", 
        "Qty", "Revenue", "Cost", "Status", "Delivery_Days"
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"❌ Validation Failed! Missing columns: {missing_columns}")
        return  # Stop here so we don't break the database

    # 4. Clean & Prep (Sidi Ghanem Strategy)
    # Strip whitespace from all text columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Force correct data types
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

    # Fill missing values
    df.fillna({
        "City": "Unknown",
        "Cost": 0.00,
        "Status": "Pending",
        "Delivery_Days": 0,
        "Product": "Unknown_Product",
        "Qty": 0,
        "Revenue": 0.00
    }, inplace=True)

    # 5. Ship to SQL
    logging.info(f"Uploading {len(df)} rows to Big_Logistics_Data...")
    df.to_sql('Big_Logistics_Data', con=engine, if_exists='append', index=False)
    logging.info("🚀 Success! Data is now ready for Power BI.")