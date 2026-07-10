import { useEffect, useState } from "react";
import api from "../api";

export default function Orders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/api/orders/my")
      .then(res => setOrders(res.data))
      .catch(() => setOrders([]));
  }, []);

  return (
    <div className="container">
      <h2>📦 My Orders</h2>

      {orders.length === 0 && <p>No orders found</p>}

      {orders.map(o => (
        <div className="card" key={o.id}>
          <h3>Order #{o.id}</h3>
          <p>Status: {o.status}</p>
          <p>Total: ₹{o.total_amount}</p>

          {o.items?.map(i => (
            <p key={i.id}>
              {i.product_name} - {i.quantity} x ₹{i.unit_price}
            </p>
          ))}
        </div>
      ))}
    </div>
  );
}