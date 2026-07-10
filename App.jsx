import { Routes, Route, useLocation } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import ProductDetail from "./pages/ProductDetail";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Orders from "./pages/Orders";
import Login from "./pages/Login";
import Register from "./pages/Register";

import AdminProducts from "./pages/admin/AdminProducts";
import ProductForm from "./pages/admin/ProductForm";
import AdminOrders from "./pages/admin/AdminOrders";

import AdminRoute from "./components/AdminRoute";
import { ThemeProvider } from "./context/ThemeContext";

function App() {
  const location = useLocation();

  // Login/Register page-ல Navbar hide
  const hideNavbar = false;
    location.pathname === "/login" ||
    location.pathname === "/register";

  return (
    <ThemeProvider>
      {!hideNavbar && <Navbar />}

      <Routes>
        {/* AUTH */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* HOME */}
        <Route path="/" element={<Home />} />

        {/* CUSTOMER */}
        <Route path="/product/:id" element={<ProductDetail />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/orders" element={<Orders />} />

        {/* ADMIN */}
        <Route
          path="/admin/products"
          element={
            <AdminRoute>
              <AdminProducts />
            </AdminRoute>
          }
        />

        <Route
          path="/admin/products/add"
          element={
            <AdminRoute>
              <ProductForm />
            </AdminRoute>
          }
        />

        <Route
          path="/admin/products/edit/:id"
          element={
            <AdminRoute>
              <ProductForm />
            </AdminRoute>
          }
        />

        <Route
          path="/admin/orders"
          element={
            <AdminRoute>
              <AdminOrders />
            </AdminRoute>
          }
        />
      </Routes>
    </ThemeProvider>
  );
}

export default App;