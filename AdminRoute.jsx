import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

export default function AdminRoute({ children }) {
  const { user } = useAuth();

  return user?.role === "admin"
    ? children
    : <Navigate to="/" />;
}