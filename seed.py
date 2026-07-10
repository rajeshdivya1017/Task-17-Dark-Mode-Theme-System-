import mysql.connector
from flask_bcrypt import Bcrypt
 
# =========================
# DB CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$Divya@1010",   # change if needed
    database="ecommerce"
)
 
cursor = db.cursor()
bcrypt = Bcrypt()
 
# =========================
# RESET DATABASE (SAFE ORDER)
# =========================
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
 
cursor.execute("DELETE FROM order_items")
cursor.execute("DELETE FROM orders")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM categories")
cursor.execute("DELETE FROM users")
 
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
 
# =========================
# USERS
# =========================
admin_pass = bcrypt.generate_password_hash("admin123").decode('utf-8')
user_pass = bcrypt.generate_password_hash("user123").decode('utf-8')
 
cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (%s, %s, %s, %s)
""", ("Admin", "admin@shop.com", admin_pass, "admin"))
 
cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (%s, %s, %s, %s)
""", ("User", "user@shop.com", user_pass, "customer"))
 
# =========================
# CATEGORIES
# =========================
categories = [
    ("Electronics",),
    ("Groceries",),
    ("Toys",),
    ("Beauty",),
    ("Fashion",),
    ("Books",),
    ("Home & Kitchen",),
    ("Sports",)
]
 
cursor.executemany(
    "INSERT INTO categories (name) VALUES (%s)",
    categories
)
db.commit()
 
# category map
cursor.execute("SELECT id, name FROM categories")
cat_map = {name: id for (id, name) in cursor.fetchall()}
 
# =========================
# PRODUCTS (FIXED IMAGES)
# =========================
products = [
    # ---------------- ELECTRONICS ----------------
    ("Laptop", "High performance laptop", 55000, 10, "Electronics",
     "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80"),
 
    ("Smartphone", "Latest Android phone", 25000, 20, "Electronics",
     "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80"),
 
    ("Headphones", "Noise cancelling headphones", 3000, 30, "Electronics",
     "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"),
 
    ("Smart Watch", "Fitness tracker watch", 4000, 25, "Electronics",
     "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80"),
 
    ("Bluetooth Speaker", "Portable speaker", 1500, 35, "Electronics",
     "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?auto=format&fit=crop&w=600&q=80"),
    
    
    # ---------------- GROCERIES ----------------
    ("Rice Bag", "Premium quality rice 5kg", 450, 50, "Groceries",
     "https://images.unsplash.com/photo-1603048297172-c92544798d5a?auto=format&fit=crop&w=600&q=80"),
 
    ("Wheat Flour", "Fresh wheat flour 5kg pack", 300, 40, "Groceries",
     "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80"),
 
    ("Cooking Oil", "Refined sunflower oil 1L", 180, 60, "Groceries",
     "https://images.unsplash.com/photo-1620706857370-e1b9770e8bb1?auto=format&fit=crop&w=600&q=80"),
 
    ("Sugar", "White refined sugar 1kg", 60, 80, "Groceries",
     "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=600&q=80"),
 
    # ---------------- TOYS ----------------
    ("Toy Car", "Remote car", 800, 30, "Toys",
     "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?auto=format&fit=crop&w=600&q=80"),
 
    ("Lego Set", "Building blocks", 1200, 25, "Toys",
     "https://images.unsplash.com/photo-1587654780291-39c9404d746b?auto=format&fit=crop&w=600&q=80"),
 
    ("Doll", "Kids doll", 500, 40, "Toys",
     "https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&w=600&q=80"),
 
    # ---------------- BEAUTY ----------------
    ("Lipstick", "Matte lipstick", 250, 60, "Beauty",
     "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=600&q=80"),
 
    ("Face Cream", "Skin care cream", 350, 45, "Beauty",
     "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=600&q=80"),
 
    ("Perfume", "Luxury perfume", 1200, 30, "Beauty",
     "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=600&q=80"),
 
    # ---------------- FASHION ----------------
    ("T-Shirt", "Cotton shirt", 500, 50, "Fashion",
     "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=600&q=80"),
 
    ("Jeans", "Slim fit jeans", 1200, 40, "Fashion",
     "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=600&q=80"),
 
    ("Shoes", "Running shoes", 2000, 35, "Fashion",
     "https://images.unsplash.com/photo-1528701800489-20be3c4ea4f2?auto=format&fit=crop&w=600&q=80"),
 
    # ---------------- BOOKS ----------------
    ("Python Book", "Learn Python", 500, 30, "Books",
     "https://images.unsplash.com/photo-1512820790803-83ca734da9c0?auto=format&fit=crop&w=600&q=80"),
 
    ("AI Basics", "AI introduction", 600, 20, "Books",
     "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=600&q=80"),
 
    # ---------------- HOME & KITCHEN ----------------
    ("Mixer Grinder", "Kitchen appliance", 2500, 20, "Home & Kitchen",
     "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=600&q=80"),
 
    ("Kettle", "Electric kettle", 900, 30, "Home & Kitchen",
     "https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=600&q=80"),
 
    ("Water Bottle", "Steel bottle", 300, 50, "Home & Kitchen",
     "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=600&q=80"),
 
    # ---------------- SPORTS ----------------
    ("Football", "Sports ball", 800, 40, "Sports",
     "https://images.unsplash.com/photo-1575361204480-aadea25e6e68?auto=format&fit=crop&w=600&q=80"),
 
    ("Cricket Bat", "Pro bat", 1500, 25, "Sports",
     "https://images.unsplash.com/photo-1593766788306-28561a7e95b0?auto=format&fit=crop&w=600&q=80"),
 
    ("Basketball", "Indoor ball", 900, 30, "Sports",
     "https://images.unsplash.com/photo-1519861531473-9200262188bf?auto=format&fit=crop&w=600&q=80"),

    # ---------------- ELECTRONICS ----------------
("Gaming Mouse", "RGB wired gaming mouse", 1800, 25, "Electronics",
"https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=600&q=80"),

("Mechanical Keyboard", "RGB mechanical keyboard", 3500, 18, "Electronics",
"https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?auto=format&fit=crop&w=600&q=80"),

("Power Bank", "20000mAh fast charging power bank", 2200, 30, "Electronics",
"https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80"),

("Webcam", "HD USB webcam", 2800, 20, "Electronics",
"https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?auto=format&fit=crop&w=600&q=80"),

("USB Flash Drive", "64GB USB 3.0 pendrive", 900, 40, "Electronics",
"https://images.unsplash.com/photo-1587033411391-5d9e51cce126?auto=format&fit=crop&w=600&q=80"),

# ---------------- GROCERIES ----------------
("Green Tea", "Organic green tea leaves", 220, 60, "Groceries",
"https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=600&q=80"),

("Honey", "Pure natural honey", 450, 35, "Groceries",
"https://images.unsplash.com/photo-1587049352851-8d4e89133924?auto=format&fit=crop&w=600&q=80"),

("Pasta", "Italian pasta pack", 180, 50, "Groceries",
"https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=600&q=80"),

("Oats", "Healthy breakfast oats", 260, 45, "Groceries",
"https://images.unsplash.com/photo-1515543904379-3d757afe72e2?auto=format&fit=crop&w=600&q=80"),

("Peanut Butter", "Creamy peanut butter jar", 320, 30, "Groceries",
"https://images.unsplash.com/photo-1621939514649-280e2ee25f60?auto=format&fit=crop&w=600&q=80"),

# ---------------- TOYS ----------------
("Teddy Bear", "Soft teddy bear for kids", 750, 25, "Toys",
"https://images.unsplash.com/photo-1563901935883-cb0f5be87079?auto=format&fit=crop&w=600&q=80"),

("Puzzle Cube", "3x3 speed cube puzzle", 350, 40, "Toys",
"https://images.unsplash.com/photo-1591994843349-f415893b3a6b?auto=format&fit=crop&w=600&q=80"),

("Chess Board", "Wooden chess board set", 950, 20, "Toys",
"https://images.unsplash.com/photo-1528819622765-d6bcf132f793?auto=format&fit=crop&w=600&q=80"),

("Building Blocks", "Creative building blocks set", 1400, 22, "Toys",
"https://images.unsplash.com/photo-1587654780291-39c9404d746b?auto=format&fit=crop&w=600&q=80"),

("RC Helicopter", "Remote control helicopter", 2600, 15, "Toys",
"https://images.unsplash.com/photo-1473968512647-3e447244af8f?auto=format&fit=crop&w=600&q=80"),

# ---------------- BEAUTY ----------------
("Face Wash", "Gentle daily face wash", 280, 50, "Beauty",
"https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=600&q=80"),

("Shampoo", "Herbal hair shampoo", 420, 45, "Beauty",
"https://images.unsplash.com/photo-1526947425960-945c6e72858f?auto=format&fit=crop&w=600&q=80"),

("Conditioner", "Smooth hair conditioner", 450, 35, "Beauty",
"https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=600&q=80"),

("Body Lotion", "Moisturizing body lotion", 380, 40, "Beauty",
"https://images.unsplash.com/photo-1619451334792-150fd785ee74?auto=format&fit=crop&w=600&q=80"),

("Sunscreen", "SPF 50 sunscreen lotion", 520, 30, "Beauty",
"https://images.unsplash.com/photo-1556228578-dd6b4741f87a?auto=format&fit=crop&w=600&q=80"),

# ---------------- FASHION ----------------
("Hoodie", "Warm cotton hoodie", 1200, 30, "Fashion",
"https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=600&q=80"),

("Formal Shirt", "Premium formal shirt", 950, 25, "Fashion",
"https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=600&q=80"),

("Jacket", "Winter casual jacket", 2200, 20, "Fashion",
"https://images.unsplash.com/photo-1520975916090-3105956dac38?auto=format&fit=crop&w=600&q=80"),

("Sneakers", "Comfortable casual sneakers", 2800, 18, "Fashion",
"https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80"),

("Cap", "Adjustable sports cap", 450, 40, "Fashion",
"https://images.unsplash.com/photo-1521369909029-2afed882baee?auto=format&fit=crop&w=600&q=80"),

# ---------------- BOOKS ----------------
("Java Programming", "Complete Java programming guide", 650, 25, "Books",
"https://images.unsplash.com/photo-1512820790803-83ca734da9c0?auto=format&fit=crop&w=600&q=80"),

("Web Development", "HTML CSS JavaScript guide", 720, 20, "Books",
"https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=600&q=80"),

("SQL Essentials", "Learn SQL from basics", 580, 28, "Books",
"https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=80"),

("Machine Learning", "Introduction to Machine Learning", 850, 18, "Books",
"https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=80"),

("Data Structures", "DSA concepts and examples", 700, 22, "Books",
"https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=600&q=80"),

# ---------------- HOME & KITCHEN ----------------
("Air Fryer", "Healthy oil-free cooking", 5500, 15, "Home & Kitchen",
"https://images.unsplash.com/photo-1585515656973-6c4d6e59df13?auto=format&fit=crop&w=600&q=80"),

("Rice Cooker", "Automatic electric rice cooker", 2400, 20, "Home & Kitchen",
"https://images.unsplash.com/photo-1586201375761-83865001e17c?auto=format&fit=crop&w=600&q=80"),

("Pressure Cooker", "5L stainless steel cooker", 1800, 22, "Home & Kitchen",
"https://images.unsplash.com/photo-1565538810643-b5bdb714032a?auto=format&fit=crop&w=600&q=80"),

("Toaster", "2-slice bread toaster", 1600, 25, "Home & Kitchen",
"https://images.unsplash.com/photo-1585238342024-78d387f4a707?auto=format&fit=crop&w=600&q=80"),

("Blender", "Multi-purpose kitchen blender", 3200, 18, "Home & Kitchen",
"https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=600&q=80"),

# ---------------- SPORTS ----------------
("Tennis Racket", "Professional tennis racket", 3500, 15, "Sports",
"https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?auto=format&fit=crop&w=600&q=80"),

("Yoga Mat", "Non-slip yoga mat", 950, 35, "Sports",
"https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=600&q=80"),

("Badminton Racket", "Lightweight badminton racket", 1800, 20, "Sports",
"https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=600&q=80"),

("Boxing Gloves", "Training boxing gloves", 2100, 18, "Sports",
"https://images.unsplash.com/photo-1517438476312-10d79c077509?auto=format&fit=crop&w=600&q=80"),

("Cricket Helmet", "Protective cricket helmet", 1900, 20, "Sports",
"https://images.unsplash.com/photo-1624880357913-a8539238245b?auto=format&fit=crop&w=600&q=80"),

# ---------------- ELECTRONICS ----------------
("Wireless Charger", "Fast wireless charging pad", 1800, 20, "Electronics",
"https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=600&q=80"),

("Noise Cancelling Earbuds", "True wireless earbuds", 4999, 18, "Electronics",
"https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?auto=format&fit=crop&w=600&q=80"),

# ---------------- GROCERIES ----------------
("Almonds", "Premium California almonds 500g", 650, 40, "Groceries",
"https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=600&q=80"),

("Coffee Powder", "Premium roasted coffee powder", 380, 35, "Groceries",
"https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80"),

# ---------------- TOYS ----------------
("Remote Control Boat", "Battery operated RC boat", 2800, 12, "Toys",
"https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&w=600&q=80"),

("Kids Train Set", "Electric toy train set", 2200, 15, "Toys",
"https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?auto=format&fit=crop&w=600&q=80"),

# ---------------- BEAUTY ----------------
("Hair Serum", "Smooth and shiny hair serum", 550, 30, "Beauty",
"https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80"),

("Makeup Kit", "Complete beauty makeup kit", 1800, 20, "Beauty",
"https://images.unsplash.com/photo-1596704017254-9d5c1b8dfc07?auto=format&fit=crop&w=600&q=80"),

# ---------------- FASHION ----------------
("Leather Belt", "Premium genuine leather belt", 850, 30, "Fashion",
"https://images.unsplash.com/photo-1624222247344-550fb60583dc?auto=format&fit=crop&w=600&q=80"),

("Track Pants", "Comfortable sports track pants", 950, 25, "Fashion",
"https://images.unsplash.com/photo-1506629905607-d9f3b1d6d84c?auto=format&fit=crop&w=600&q=80"),

# ---------------- BOOKS ----------------
("Cloud Computing", "Beginner's guide to cloud computing", 780, 20, "Books",
"https://images.unsplash.com/photo-1512820790803-83ca734da9c0?auto=format&fit=crop&w=600&q=80"),

("Cyber Security", "Fundamentals of cyber security", 820, 18, "Books",
"https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=600&q=80"),

# ---------------- HOME & KITCHEN ----------------
("Vacuum Cleaner", "Powerful home vacuum cleaner", 6500, 12, "Home & Kitchen",
"https://images.unsplash.com/photo-1558317374-067fb5f30001?auto=format&fit=crop&w=600&q=80"),

# ---------------- SPORTS ----------------
("Skipping Rope", "Adjustable fitness skipping rope", 450, 40, "Sports",
"https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=600&q=80"),
]
# =========================
# INSERT PRODUCTS
# =========================
for name, desc, price, stock, cat, img in products:
    cursor.execute("""
        INSERT INTO products (name, description, price, stock, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, desc, price, stock, cat_map[cat], img))
 
db.commit()
 
cursor.close()
db.close()
 
print(" Seed completed successfully (NO ERRORS + IMAGES FIXED PROPERLY)")