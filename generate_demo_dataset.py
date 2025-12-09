import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
CLOUD_PROVIDER = "AWS"  # Amazon Web Services
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1
TARGET_ROWS = 2000

# AWS Services (realistic service names)
SERVICES = [
    "EC2/Compute",
    "S3/Storage",
    "RDS/Database",
    "Lambda/Functions",
    "CloudFront/CDN",
    "VPC/Networking",
    "EBS/Storage",
    "ElastiCache/Cache"
]

# AWS Regions
REGIONS = [
    "us-east-1",      # N. Virginia
    "us-west-2",      # Oregon
    "eu-west-1",      # Ireland
    "ap-southeast-1",  # Singapore
    "ap-south-1"      # Mumbai
]

# Project Tags
PROJECT_TAGS = [
    "Project:Production",
    "Project:Development",
    "Project:Testing",
    "Project:Staging",
    "Project:Marketing",
    "Project:Finance",
    "Project:Analytics",
    "Project:Backup"
]

# Generate dates
dates = [START_DATE + timedelta(days=i) for i in range(TOTAL_DAYS)]

# Initialize data list
data = []

# Generate realistic cost patterns
np.random.seed(42)
random.seed(42)

# Base costs per service (in INR)
base_costs = {
    "EC2/Compute": 1200,
    "S3/Storage": 300,
    "RDS/Database": 800,
    "Lambda/Functions": 150,
    "CloudFront/CDN": 400,
    "VPC/Networking": 200,
    "EBS/Storage": 250,
    "ElastiCache/Cache": 180
}

# Generate data
row_count = 0
target_rows = TARGET_ROWS

for date in dates:
    if row_count >= target_rows:
        break
    
    # Determine how many services are active on this date
    # More services active on weekdays
    is_weekend = date.weekday() >= 5
    num_services = random.randint(3, 6) if not is_weekend else random.randint(2, 4)
    
    # Select random services for this date
    active_services = random.sample(SERVICES, min(num_services, len(SERVICES)))
    
    for service in active_services:
        if row_count >= target_rows:
            break
            
        # Select random region and tag
        region = random.choice(REGIONS)
        tag = random.choice(PROJECT_TAGS)
        
        # Base cost for this service
        base_cost = base_costs[service]
        
        # Add seasonal variation (higher in certain months)
        month_factor = 1.0
        if date.month in [11, 12, 1]:  # Holiday season
            month_factor = 1.3
        elif date.month in [6, 7, 8]:  # Summer
            month_factor = 1.15
        
        # Add weekday/weekend variation
        day_factor = 0.7 if is_weekend else 1.0
        
        # Add some trend (gradual increase over time)
        days_from_start = (date - START_DATE).days
        trend_factor = 1 + (days_from_start / 1000) * 0.2  # 20% increase over period
        
        # Add random variation
        random_factor = np.random.normal(1.0, 0.25)
        random_factor = max(0.3, min(2.0, random_factor))  # Cap between 0.3 and 2.0
        
        # Calculate final cost
        cost = base_cost * month_factor * day_factor * trend_factor * random_factor
        
        # Add occasional spikes (anomalies)
        if random.random() < 0.05:  # 5% chance of spike
            cost *= random.uniform(2.0, 5.0)
        
        # Round to 2 decimal places
        cost = round(cost, 2)
        
        data.append({
            'UsageDate': date.strftime('%Y-%m-%d'),
            'ServiceName': service,
            'Region': region,
            'ProjectTag': tag,
            'CostINR': cost
        })
        
        row_count += 1

# Create DataFrame
df = pd.DataFrame(data)

# Shuffle to make it more realistic
df = df.sample(frac=1).reset_index(drop=True)

# Sort by date
df = df.sort_values('UsageDate').reset_index(drop=True)

# Save to CSV
output_file = 'demo_aws_cost_data.csv'
df.to_csv(output_file, index=False)

print(f"✅ Generated {len(df)} rows of AWS cost data")
print(f"📅 Date range: {df['UsageDate'].min()} to {df['UsageDate'].max()}")
print(f"☁️  Cloud Provider: {CLOUD_PROVIDER}")
print(f"📊 Services: {len(df['ServiceName'].unique())} unique services")
print(f"🌍 Regions: {len(df['Region'].unique())} regions")
print(f"🏷️  Tags: {len(df['ProjectTag'].unique())} project tags")
print(f"💰 Total Cost: ₹{df['CostINR'].sum():,.2f}")
print(f"📁 Saved to: {output_file}")
print("\n📋 Service breakdown:")
print(df.groupby('ServiceName')['CostINR'].agg(['count', 'sum']).to_string())
print("\n🌍 Region breakdown:")
print(df.groupby('Region')['CostINR'].agg(['count', 'sum']).to_string())

