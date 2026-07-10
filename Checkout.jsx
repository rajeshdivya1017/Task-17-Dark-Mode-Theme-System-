import { useCart } from "../context/CartContext";

export default function Checkout() {
  const { cartItems } = useCart();

  const total = cartItems.reduce(
    (sum, i) => sum + i.price * i.qty,
    0
  );

  return (
    <div className="container">
      <h2>💳 Checkout</h2>

      {cartItems.map(i => (
        <p key={i.id}>
          {i.name} - {i.qty} x ₹{i.price}
        </p>
      ))}

      <h3>Total: ₹ {total}</h3>

      <button>Proceed Payment (Mock)</button>
    </div>
  );
}