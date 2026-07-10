import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import api from "../api";
import TokenCountdown from "./TokenCountdown";
import { useTheme } from "../context/ThemeContext";

export default function Navbar() {
  const { cartItems = [] } = useCart();
  const { user, setUser } = useAuth();
  const navigate = useNavigate();

  const { theme, toggleTheme } = useTheme();

  const totalItems = cartItems.reduce(
    (sum, item) => sum + (item.qty || 1),
    0
  );

  const logout = async () => {
    try {
      await api.get("/api/logout");
    } catch (err) {
      console.log(err);
    }

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");

    setUser(null);
    navigate("/login");
  };

  return (
    <div className="navbar">
      <h2>🛒 E-Commerce</h2>

      <div className="nav-links">
        <Link to="/">Home</Link>

        {user?.role !== "admin" && (
          <>
            <Link to="/cart">
              Cart ({totalItems})
            </Link>

            <Link to="/orders">
              My Orders
            </Link>
          </>
        )}

        {user?.role === "admin" && (
          <>
            <Link to="/admin/products">
              Products
            </Link>

            <Link to="/admin/orders">
              Orders
            </Link>
          </>
        )}

        {/* Theme button - Always visible */}
        <button
          className="btn-nav"
          onClick={toggleTheme}
        >
          {theme === "light" ? "🌙 Dark" : "☀️ Light"}
        </button>

        {!user ? (
          <Link to="/login">Login</Link>
        ) : (
          <>
            <span
              style={{
                fontWeight: "bold",
                marginRight: "10px",
              }}
            >
              👤 {user.name}
            </span>

            <TokenCountdown />

            <button
              className="logout-btn"
              onClick={logout}
            >
              Logout
            </button>
          </>
        )}
      </div>
    </div>
  );
}