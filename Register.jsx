import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [data, setData] = useState({
    name: "",
    email: "",
    password: "",
    role: "customer"   // default role
  });

  const navigate = useNavigate();

  const register = async () => {
    try {
      await api.post("/api/register", data);

      alert("Registered successfully");

      // after register go to login
      navigate("/login");

    } catch (err) {
      alert(err.response?.data?.message || "Register failed");
    }
  };

  return (
    <div className="auth-page">

      {/* BRAND TITLE */}
      <div className="brand-title">
        🛒 E-COMMERCE
      </div>

      <div className="auth-box">

        <h2>Register</h2>

        <input
          placeholder="Name"
          onChange={(e) =>
            setData({ ...data, name: e.target.value })
          }
        />

        <input
          placeholder="Email"
          onChange={(e) =>
            setData({ ...data, email: e.target.value })
          }
        />

        <input
          placeholder="Password"
          type="password"
          onChange={(e) =>
            setData({ ...data, password: e.target.value })
          }
        />

        {/* ROLE SELECTION */}
        <select
          onChange={(e) =>
            setData({ ...data, role: e.target.value })
          }
          value={data.role}
          style={{
            width: "100%",
            padding: "10px",
            marginTop: "8px",
            borderRadius: "8px",
            border: "1px solid #ddd"
          }}
        >
          <option value="customer">Customer</option>
          <option value="admin">Admin</option>
        </select>

        <button onClick={register}>
          Register
        </button>

        {/* LOGIN LINK */}
        <p className="auth-link">
          Already have an account?{" "}
          <Link to="/login">Login</Link>
        </p>

      </div>
    </div>
  );
}