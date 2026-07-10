import { useEffect, useState } from "react";
import api from "../../api";
import Pagination from "../../components/Pagination";

export default function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const limit = 10;

  const loadOrders = async (currentPage = page) => {
    try {
      const res = await api.get("/api/admin/orders", {
        params: {
          page: currentPage,
          limit,
        },
      });

      setOrders(res.data.orders);
      setTotalPages(res.data.total_pages);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    loadOrders(page);
  }, [page]);

  const updateStatus = async (id, status) => {
    try {
      await api.put(`/api/orders/${id}/status`, { status });

      // Reload current page after updating status
      loadOrders(page);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="container">
      <h2>Admin Orders</h2>

      {orders.length > 0 ? (
        <>
          {orders.map((o) => (
            <div className="card" key={o.id}>
              <h3>Order #{o.id}</h3>

              <p>
                <strong>Customer:</strong> {o.customer_name}
              </p>

              <p>
                <strong>Total:</strong> ₹{o.total_amount}
              </p>

              <p>
                <strong>Address:</strong> {o.address}
              </p>

              <p>
                <strong>Status:</strong>
              </p>

              <select
                value={o.status}
                onChange={(e) =>
                  updateStatus(o.id, e.target.value)
                }
              >
                <option value="Pending">Pending</option>
                <option value="Confirmed">Confirmed</option>
                <option value="Shipped">Shipped</option>
                <option value="Delivered">Delivered</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
          ))}

          <Pagination
            currentPage={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        </>
      ) : (
        <p>No orders found.</p>
      )}
    </div>
  );
}