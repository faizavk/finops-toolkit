# Configuration for Dataset
# Update these if your CSV has different column names

# CSV File Configuration
CSV_FILE_NAME = 'ideal_cost_data.csv'  # Change this to your CSV filename

# Column Name Configuration
# If your CSV has different column names, update these:
COLUMN_DATE = 'UsageDate'        # Your date column name
COLUMN_SERVICE = 'ServiceName'   # Your service column name
COLUMN_REGION = 'Region'         # Your region column name
COLUMN_TAG = 'ProjectTag'        # Your tag/project column name
COLUMN_COST = 'CostINR'          # Your cost column name

# Note: If you change these, you'll also need to update app.py
# to use these constants instead of hardcoded strings

