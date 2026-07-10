import { useEffect, useState } from "react";
import api from "../api";
import { useCart } from "../context/CartContext";
import { useDebounce } from "../hooks/useDebounce";
import Pagination from "../components/Pagination";

export default function Home() {
  const { addToCart } = useCart();

  const [products, setProducts] = useState([]);

  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search, 300);

  const [category, setCategory] = useState("");

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const limit = 8;

  useEffect(() => {
    loadProducts();
  }, [page, debouncedSearch, category]);

  const loadProducts = async () => {
  try {
    const res = await api.get("/api/products", {
      params: {
        page,
        limit,
        search: debouncedSearch,
        category,   
      },
    });

    setProducts(res.data.products);
    setTotalPages(res.data.total_pages);
  } catch (err) {
    console.log(err);
  }
};

  // Reset page when searching
  useEffect(() => {
    setPage(1);
  }, [debouncedSearch, category]);

  
  return (
    <div className="container">

      <h2 className="page-title">🛍️ Products</h2>

      {/* Search */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px",
          flexWrap: "wrap",
        }}
      >
        <input
          type="text"
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            flex: 1,
            minWidth: "250px",
            padding: "10px",
          }}
        />

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{
            padding: "10px",
          }}
        >
          <option value="">All Categories</option>
          <option value="Electronics">Electronics</option>
          <option value="Groceries">Groceries</option>
          <option value="Toys">Toys</option>
          <option value="Beauty">Beauty</option>
          <option value="Fashion">Fashion</option>
          <option value="Books">Books</option>
          <option value="Home & Kitchen">Home & Kitchen</option>
          <option value="Sports">Sports</option>
        </select>
      </div>

      {debouncedSearch && (
        <p style={{ marginBottom: "15px" }}>
          🔍 Searching for <b>{debouncedSearch}</b>
        </p>
      )}

      <div className="product-grid">

        {products.length > 0 ? (
          products.map((product) => (
            <div
              className="product-card"
              key={product.id}
            >
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
                  objectFit: "cover",
                }}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src =
                    "https://placehold.co/300x300?text=No+Image";
                }}
              />

              <h3>{product.name}</h3>

              <p>₹ {product.price}</p>

              <p>{product.category}</p>

              <button
                className="btn"
                onClick={() => {
                  addToCart(product, 1);
                  alert("Added to cart 🛒");
                }}
              >
                Add to Cart
              </button>
            </div>
          ))
        ) : (
          <p>No products found 😢</p>
        )}

      </div>

      <Pagination
        currentPage={page}
        totalPages={totalPages}
        onPageChange={setPage}
      />

    </div>
  );
}