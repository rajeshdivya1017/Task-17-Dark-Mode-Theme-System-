import { useEffect, useState } from "react";
import api from "../../api";
import { Link } from "react-router-dom";


export default function AdminProducts() {
  const [products, setProducts] = useState([]);

 const load = async () => {
  try {
    const res = await api.get("/api/products", {
      params: {
        page: 1,
        limit: 1000,
        search: "",
      },
    });

    setProducts(res.data.products || []);
  } catch (err) {
    console.log(err);
    alert("Failed to load products");
  }
};
  useEffect(() => {
    load();
  }, []);

  const deleteProduct = async (id) => {
    try {
      await api.delete(`/api/products/${id}`);
      load();
    } catch (err) {
      alert("Delete failed");
    }
  };

  return (
    <div className="container">

      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Admin Products</h2>

        <Link to="/admin/products/add">
          <button>Add Product</button>
        </Link>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3,1fr)",
          gap: "15px"
        }}
      >

        {products.map(product => (
          <div
            key={product.id}
            className="card"
            style={{
              border: "1px solid #ddd",
              padding: "10px",
              borderRadius: "8px"
            }}
          >

            {/* ✅ FIXED IMAGE */}
           <img
  src={
    product.image_url
      ? `http://localhost:5000${product.image_url}`
      : "https://placehold.co/300x300?text=No+Image"
  }
  alt={product.name}
  style={{
    width: "100%",
    height: "200px",
    objectFit: "cover"
  }}
  onError={(e) => {
    e.target.onerror = null;
    e.target.src = "https://placehold.co/300x300?text=No+Image";
  }}
/>

            <h3>{product.name}</h3>
            <p>₹ {product.price}</p>

            <div style={{ display: "flex", gap: "10px" }}>
              <Link to={`/admin/products/edit/${product.id}`}>
                <button>Edit</button>
              </Link>

              <button onClick={() => deleteProduct(product.id)}>
                Delete
              </button>
            </div>

          </div>
        ))}

      </div>
    </div>
  );
}