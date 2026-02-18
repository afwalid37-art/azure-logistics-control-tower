import pandas as pd
import random
import datetime

print("🚀 Generating Enterprise Data...")

# 1. Setup Lists
cities = ["Casablanca", "Marrakech", "Tanger", "Agadir", "Rabat", "Fes", "Oujda"]
# Updated Product List with 20+ Items
products = {
    # High-End Tech
    "Laptop Dell XPS": 18000,
    "MacBook Pro M3": 24000,
    "iPhone 15 Pro": 13500,
    "iPad Air": 7500,
    "Samsung Galaxy S24": 11000,
    
    # Home Appliances (High Volume)
    "Machine à Laver Samsung": 4500,
    "Réfrigérateur LG": 8000,
    "Air Fryer Ninja": 1800,
    "Robot Aspirateur Xiaomi": 3200,
    "Machine à Café Nespresso": 1500,
    "Blender Hofmann": 600,  # Realistic local item
    
    # Gaming & Entertainment
    "Sony PlayStation 5": 6500,
    "Xbox Series X": 5800,
    "TV Samsung 55' 4K": 5500,
    "Casque Gamer HyperX": 900,
    "Chaise Gaming Drift": 2200,
    
    # Accessories & Gadgets
    "Apple Watch Series 9": 4500,
    "AirPods Pro 2": 2800,
    "Imprimante HP LaserJet": 2500,
    "Disque Dur Externe 1TB": 550,
    "Trottinette Électrique Xiaomi": 4200,
    "GoPro Hero 12": 5000,
    "Drone DJI Mini": 6000
}
status_list = ["Delivered", "Delivered", "Delivered", "Pending", "Returned", "Cancelled"]

data = []
start_date = datetime.date(2025, 1, 1)

# 2. Generate 10,000 Rows
for i in range(100):
    order_id = f"ORD-{199999+i}"
    date = start_date + datetime.timedelta(days=random.randint(0, 365))
    city = random.choice(cities)
    product_name = random.choice(list(products.keys()))
    price = products[product_name]
    qty = random.randint(1, 5)
    
    # Logic: Cost is 70% of Price (30% Margin)
    cost = price * 0.7
    total_revenue = price * qty
    total_cost = cost * qty
    
    status = random.choice(status_list)
    
    # Delivery Logic
    shipping_days = random.randint(1, 15) # 15 days is bad!
    delivery_date = date + datetime.timedelta(days=shipping_days)
    
    data.append([order_id, date, city, product_name, qty, total_revenue, total_cost, status, shipping_days])

# 3. Save to CSV
df = pd.DataFrame(data, columns=[
    "Order_ID", "Order_Date", "City", "Product", "Qty", "Revenue", "Cost", "Status", "Delivery_Days"
])

df.to_csv("Big_Logistics_Data.csv", index=False)
print(f"✅ Generated {len(df)} rows of data in 'Big_Logistics_Data.csv'")