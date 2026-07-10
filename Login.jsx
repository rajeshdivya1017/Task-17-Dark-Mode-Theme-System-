import { useState } from "react";
import api from "../api";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const { setUser } = useAuth();
  const navigate = useNavigate();

  const login = async () => {
    if (loading) return;

    setLoading(true);

    try {
      const res = await api.post("/api/login", {
        email,
        password,
      });

      // Save JWT Tokens
      localStorage.setItem(
        "access_token",
        res.data.access_token
      );

      localStorage.setItem(
        "refresh_token",
        res.data.refresh_token
      );

      // Save User
      localStorage.setItem(
        "user",
        JSON.stringify(res.data.user)
      );

      setUser(res.data.user);

      if (res.data.user.role === "admin") {
        navigate("/admin/products");
      } else {
        navigate("/");
      }
    } catch (err) {
      alert(err.response?.data?.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-box">
        <h2>Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={login} disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="auth-link">
          <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}