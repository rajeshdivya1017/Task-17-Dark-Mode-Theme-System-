import { useCart } from "../context/CartContext";
import api from "../api";
import { useState } from "react";

export default function Cart() {
  const { cartItems = [], removeFromCart, clearCart } = useCart();
  const [address, setAddress] = useState("");

  const total = cartItems.reduce(
    (sum, i) => sum + i.price * i.qty,
    0
  );

  const placeOrder = async () => {
    try {
      const res = await api.post("/api/orders", {
        address,
        items: cartItems.map((i) => ({
          product_id: i.id,
          quantity: i.qty,
        })),
      });

      alert(res.data.message);
      clearCart();
      setAddress("");
    } catch (err) {
      alert(err.response?.data?.message || "Order failed");
    }
  };

  return (
    <div className="container">
      <h2>🛒 Cart</h2>

      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          {cartItems.map((i) => (
            <div
              key={i.id}
              className="cart-item"
              style={{
                display: "flex",
                alignItems: "center",
                gap: "20px",
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "15px",
                marginBottom: "15px",
              }}
            >
              <img
                src={`http://localhost:5000${i.image_url}`}
                alt={i.name}
                style={{
                  width: "100px",
                  height: "100px",
                  objectFit: "cover",
                  borderRadius: "8px",
                }}
              />

              <div style={{ flex: 1 }}>
                <h3>{i.name}</h3>
                <p>Price: ₹ {i.price}</p>
                <p>Quantity: {i.qty}</p>
                <p>
                  <strong>Total: ₹ {i.price * i.qty}</strong>
                </p>

                <button onClick={() => removeFromCart(i.id)}>
                  Remove
                </button>
              </div>
            </div>
          ))}

          <h3>Total Amount: ₹ {total}</h3>

          <input
            type="text"
            placeholder="Delivery Address"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "15px",
            }}
          />

          <button onClick={placeOrder}>
            Place Order
          </button>
        </>
      )}
    </div>
  );
}