
import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
 
export default function ProductCard({ product }) {
  const { addToCart } = useCart();
 
  return (
<div className="card">
      {/* FIXED: Pulling string image URL variable directly without the processing abstraction layer */}
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
<p className="category-tag">{product.category}</p>
 
      <div className="card-actions">
<Link to={`/product/${product.id}`}>
<button className="view-btn">View</button>
</Link>
 
        <button className="add-btn" onClick={() => addToCart(product, 1)}>
          Add to Cart
</button>
</div>
</div>
  );
}