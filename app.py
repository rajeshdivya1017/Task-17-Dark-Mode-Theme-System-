from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from datetime import timedelta

from db import get_connection
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# =========================
# CONFIG
# =========================


CORS(
    app,
        origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ]
)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = "ecommerce_jwt_secret"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)

app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

# =========================
# IMAGE UPLOAD CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/api/upload", methods=["POST"])
def upload_image():

    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only png, jpg, jpeg and webp allowed"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4().hex}.{ext}"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    return jsonify({
        "image_url": f"/static/uploads/{filename}"
    }), 201
# =========================
# REGISTER
# =========================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "customer")

    if not name or not email or not password:
        return jsonify({"message": "All fields required"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return jsonify({"message": "Email exists"}), 400

    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, hashed, role))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Registered"}), 201


# =========================
# LOGIN
# =========================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or not bcrypt.check_password_hash(
        user["password"],
        password
    ):
        return jsonify({"message": "Invalid login"}), 401

    access_token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "role": user["role"],
            "name": user["name"]
        }
    )

    refresh_token = create_refresh_token(
        identity=str(user["id"])
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


# =========================
# LOGOUT
# =========================
@app.route("/api/logout")
def logout():
    return jsonify({"message": "Logged out"})


# =========================
# CURRENT USER
# =========================
@app.route("/api/me")
@jwt_required()
def me():

    user_id = get_jwt_identity()

    claims = get_jwt()

    return jsonify({
        "id": int(user_id),
        "name": claims["name"],
        "role": claims["role"]
    })

# =========================
# PRODUCTS
# =========================
@app.route("/api/products")
def get_products():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 8))
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    where_clause = "WHERE p.name LIKE %s"
    params = [f"%{search}%"]

    if category:
        where_clause += " AND c.name = %s"
        params.append(category)

    # Total count
    count_query = f"""
        SELECT COUNT(*) AS total
        FROM products p
        LEFT JOIN categories c
        ON p.category_id = c.id
        {where_clause}
    """

    cursor.execute(count_query, tuple(params))
    total = cursor.fetchone()["total"]

    # Products
    product_query = f"""
        SELECT
            p.*,
            c.name AS category
        FROM products p
        LEFT JOIN categories c
        ON p.category_id = c.id
        {where_clause}
        ORDER BY p.id DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(
        product_query,
        tuple(params + [limit, offset])
    )

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "products": products,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    })
# =========================
# SINGLE PRODUCT
# =========================
@app.route("/api/products/<int:id>")
def get_product(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.*, c.name AS category
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id=%s
    """, (id,))

    product = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(product)



# =========================
# ADD PRODUCT
# =========================
@app.route("/api/products", methods=["POST"])
@jwt_required()
def add_product():

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, description, price, stock, category_id, image_url)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        data["name"],
        data.get("description"),
        data["price"],
        data["stock"],
        data["category_id"],
        data["image_url"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Product added"})


# =========================
# UPDATE PRODUCT
# =========================
@app.route("/api/products/<int:id>", methods=["PUT"])
@jwt_required()
def update_product(id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name=%s,
            description=%s,
            price=%s,
            stock=%s,
            category_id=%s,
            image_url=%s
        WHERE id=%s
    """, (
        data["name"],
        data.get("description"),
        data["price"],
        data["stock"],
        data["category_id"],
        data["image_url"],
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Updated"})

# =========================
# DELETE PRODUCT
# =========================
# =========================
# DELETE PRODUCT
# =========================
@app.route("/api/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Deleted"})

# =========================
# CREATE ORDER
# =========================
# =========================
# CREATE ORDER
# =========================
@app.route("/api/orders", methods=["POST", "OPTIONS"])
@jwt_required()
def create_order():

    if request.method == "OPTIONS":
        return "", 200

    user_id = get_jwt_identity()

    data = request.json
    address = data.get("address")
    items = data.get("items", [])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    total = 0

    for i in items:
        cursor.execute(
            "SELECT price FROM products WHERE id=%s",
            (i["product_id"],)
        )
        p = cursor.fetchone()

        if p:
            total += p["price"] * i["quantity"]

    cursor.execute("""
        INSERT INTO orders
        (user_id, total_amount, status, address)
        VALUES (%s,%s,%s,%s)
    """, (
        user_id,
        total,
        "Pending",
        address
    ))

    order_id = cursor.lastrowid

    for i in items:

        cursor.execute(
            "SELECT price FROM products WHERE id=%s",
            (i["product_id"],)
        )

        p = cursor.fetchone()

        if p:
            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
                VALUES (%s,%s,%s,%s)
            """, (
                order_id,
                i["product_id"],
                i["quantity"],
                p["price"]
            ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order placed"})
# =========================
# MY ORDERS
# =========================
@app.route("/api/orders/my")
@jwt_required()
def my_orders():

    user_id = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE user_id=%s
        ORDER BY id DESC
    """, (user_id,))

    orders = cursor.fetchall()

    for o in orders:

        cursor.execute("""
            SELECT oi.*,
                   p.name AS product_name
            FROM order_items oi
            JOIN products p
            ON oi.product_id = p.id
            WHERE oi.order_id=%s
        """, (o["id"],))

        o["items"] = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(orders)



# =========================
# ADMIN ORDERS
# =========================
@app.route("/api/admin/orders")
@jwt_required()
def admin_orders():

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM orders
    """)

    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT o.*,
               u.name AS customer_name
        FROM orders o
        JOIN users u
        ON o.user_id = u.id
        ORDER BY o.id DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "orders": orders,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    })

# =========================
# UPDATE ORDER STATUS
# =========================
@app.route("/api/orders/<int:id>/status", methods=["PUT"])
@jwt_required()
def update_order_status(id):

    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=%s WHERE id=%s",
        (data["status"], id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Order status updated successfully"
    })

# =========================
# REFRESH TOKEN
# =========================
@app.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    new_access_token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "role": user["role"],
            "name": user["name"]
        }
    )

    return jsonify({
        "access_token": new_access_token
    }), 200
# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)