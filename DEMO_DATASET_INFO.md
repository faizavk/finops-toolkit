# Demo Dataset Information

## 📊 Dataset Details

- **File Name**: `demo_aws_cost_data.csv`
- **Cloud Provider**: **AWS (Amazon Web Services)**
- **Total Rows**: 2,000
- **Date Range**: January 1, 2023 to April 24, 2024 (~480 days)
- **Total Cost**: ₹1,049,707.33

## ☁️ AWS Services Included (8 services)

1. **EC2/Compute** - Virtual servers (239 records, ₹356,281.48)
2. **S3/Storage** - Object storage (245 records, ₹91,738.62)
3. **RDS/Database** - Managed databases (242 records, ₹227,420.16)
4. **Lambda/Functions** - Serverless compute (250 records, ₹46,412.05)
5. **CloudFront/CDN** - Content delivery network (261 records, ₹136,108.80)
6. **VPC/Networking** - Virtual private cloud (274 records, ₹67,014.08)
7. **EBS/Storage** - Block storage (241 records, ₹71,022.23)
8. **ElastiCache/Cache** - In-memory caching (248 records, ₹53,709.91)

## 🌍 AWS Regions (5 regions)

1. **us-east-1** - N. Virginia (398 records, ₹202,047.57)
2. **us-west-2** - Oregon (379 records, ₹199,045.37)
3. **eu-west-1** - Ireland (382 records, ₹206,431.47)
4. **ap-southeast-1** - Singapore (440 records, ₹236,286.44)
5. **ap-south-1** - Mumbai (401 records, ₹205,896.48)

## 🏷️ Project Tags (8 tags)

- Project:Production
- Project:Development
- Project:Testing
- Project:Staging
- Project:Marketing
- Project:Finance
- Project:Analytics
- Project:Backup

## 📈 Data Characteristics

### Realistic Patterns Included:
- ✅ **Seasonal variations**: Higher costs during holiday season (Nov-Dec-Jan)
- ✅ **Weekday/Weekend patterns**: Lower costs on weekends
- ✅ **Trending growth**: Gradual cost increase over time (~20% over period)
- ✅ **Anomaly spikes**: Random cost spikes (5% of records) for anomaly detection
- ✅ **Service diversity**: Multiple AWS services with realistic cost ranges
- ✅ **Geographic distribution**: Costs across multiple AWS regions
- ✅ **Project tagging**: Costs tagged to different projects

### Perfect for Demonstrating:
1. ✅ Historical cost visualization
2. ✅ Future forecasting with Prophet
3. ✅ Anomaly detection (has built-in spikes)
4. ✅ Root Cause Analysis (multiple services/regions/tags)
5. ✅ Service-level forecasting
6. ✅ Security insights
7. ✅ Unit cost computation

## 🚀 How to Use This Dataset

### Option 1: Replace Current Dataset
```bash
# Backup current dataset
mv ideal_cost_data.csv ideal_cost_data_backup.csv

# Use demo dataset
mv demo_aws_cost_data.csv ideal_cost_data.csv

# Restart backend
cd backend
source venv/bin/activate
python app.py
```

### Option 2: Update Code to Use Demo Dataset
Edit `backend/app.py` line 24:
```python
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demo_aws_cost_data.csv')
```

## 📊 Sample Data Preview

```csv
UsageDate,ServiceName,Region,ProjectTag,CostINR
2023-01-01,EC2/Compute,us-east-1,Project:Production,1456.23
2023-01-01,S3/Storage,ap-south-1,Project:Development,312.45
2023-01-01,RDS/Database,eu-west-1,Project:Testing,987.67
...
```

## 🎯 Why This Dataset is Great for Demo

1. **Realistic AWS Services**: Uses actual AWS service names
2. **Good for Forecasting**: Has clear trends and patterns
3. **Anomaly Detection Ready**: Contains built-in cost spikes
4. **RCA Ready**: Multiple dimensions (services, regions, tags)
5. **Sufficient Data**: 2,000 rows over ~16 months
6. **Balanced Distribution**: Good mix across all dimensions

## 📝 Notes

- All costs are in **INR (Indian Rupees)**
- Dates follow **YYYY-MM-DD** format
- Data includes realistic variations and patterns
- Perfect for demonstrating all 10 features of the FinOps Toolkit

