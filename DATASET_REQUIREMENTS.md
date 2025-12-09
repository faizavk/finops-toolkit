# Dataset Requirements for FinOps Toolkit

## 📋 Required CSV Format

Your dataset **MUST** have these exact column names:

| Column Name | Type | Description | Required |
|------------|------|-------------|----------|
| `UsageDate` | Date/String | Date of the cost record | ✅ Yes |
| `ServiceName` | String | Name of the cloud service | ✅ Yes |
| `Region` | String | Cloud region | ✅ Yes |
| `ProjectTag` | String | Project or tag identifier | ✅ Yes |
| `CostINR` | Number | Cost amount (can be any currency) | ✅ Yes |

## 📝 Current Dataset Location

The project currently expects the dataset at:
```
/Users/summaiya.sarvari/Desktop/fin/ideal_cost_data.csv
```

## ✅ What Will Work Automatically

If your new dataset has **the same column names**, the project will work without any code changes:

- ✅ Historical cost visualization
- ✅ Forecasting
- ✅ Anomaly detection
- ✅ Root Cause Analysis (RCA)
- ✅ Unit cost computation
- ✅ Security insights
- ✅ Service-level forecasting

## ⚠️ What You Need to Change

### Option 1: Rename Your Columns (Easiest)

If your dataset has different column names, rename them to match:

**Example:**
- Your dataset has: `Date`, `Service`, `Location`, `Tag`, `Cost`
- Rename to: `UsageDate`, `ServiceName`, `Region`, `ProjectTag`, `CostINR`

### Option 2: Update the Code (If You Can't Rename)

If you can't rename columns, you'll need to update `backend/app.py`:

1. **Change the file path** (line 24):
   ```python
   DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'your_new_file.csv')
   ```

2. **Update column names** throughout the file:
   - Replace `UsageDate` with your date column name
   - Replace `ServiceName` with your service column name
   - Replace `Region` with your region column name
   - Replace `ProjectTag` with your tag column name
   - Replace `CostINR` with your cost column name

## 🔧 Quick Guide: Using a Different Dataset

### Step 1: Prepare Your Dataset
- Ensure it's a CSV file
- Has the 5 required columns (or rename them)
- Date column should be in format: `YYYY-MM-DD` or similar

### Step 2: Replace the File
- Place your CSV file in the project root: `/Users/summaiya.sarvari/Desktop/fin/`
- Either:
  - **Option A**: Rename your file to `ideal_cost_data.csv` (replaces existing)
  - **Option B**: Update `app.py` line 24 to point to your file name

### Step 3: Restart Backend
```bash
# Stop the backend (Ctrl+C)
# Then restart:
cd backend
source venv/bin/activate
python app.py
```

## 📊 Example Dataset Format

```csv
UsageDate,ServiceName,Region,ProjectTag,CostINR
2023-01-01,EC2/VMs,ap-south-1,Project:Marketing,1155.06
2023-01-01,S3/Storage,ap-south-1,Project:Marketing,270.35
2023-01-02,EC2/VMs,eu-central-1,Project:Dev,1073.87
```

## 💡 Tips

1. **Date Format**: The code uses `pd.to_datetime()` which is flexible, but `YYYY-MM-DD` works best
2. **Cost Column**: Can be any currency (USD, EUR, etc.) - just keep the column name as `CostINR` or update the code
3. **Missing Data**: The code handles missing values, but too many missing dates might affect forecasting
4. **Data Volume**: Works with any amount of data, but more data = better forecasts

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| "Column not found" error | Check column names match exactly |
| "Date parsing error" | Ensure date format is recognizable |
| "No data" in charts | Check CSV file path is correct |
| Forecast fails | Ensure you have at least 7 days of data |

## 📞 Need Help?

If your dataset has a different structure, you can:
1. Share your column names and I'll help update the code
2. Use a CSV editor to rename columns to match
3. Create a mapping script to transform your data

