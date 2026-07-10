import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import { useCart } from "../context/CartContext";


export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [qty, setQty] = useState(1);
  const { addToCart } = useCart();

  useEffect(() => {
    api.get(`/api/products/${id}`)
      .then(res => setProduct(res.data))
      .catch(err => console.log(err));
  }, [id]);

  if (!product) return <p>Loading...</p>;

  return (
    <div className="container">

      <h2>{product.name}</h2>

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

      <p>{product.description}</p>
      <h3>₹ {product.price}</h3>
      <p>Stock: {product.stock}</p>

      <input
        type="number"
        value={qty}
        min="1"
        onChange={(e) => setQty(Number(e.target.value))}
      />

      <button onClick={() => addToCart(product, qty)}>
        Add to Cart
      </button>

    </div>
  );
}