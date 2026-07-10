import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";

export default function TokenCountdown() {
  const [timeLeft, setTimeLeft] = useState("");

  useEffect(() => {
    const updateCountdown = () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setTimeLeft("");
        return;
      }

      try {
        const decoded = jwtDecode(token);

        const now = Math.floor(Date.now() / 1000);
        const remaining = decoded.exp - now;

        if (remaining <= 0) {
          setTimeLeft("Expired");
          return;
        }

        const minutes = Math.floor(remaining / 60);
        const seconds = remaining % 60;

        setTimeLeft(`${minutes}m ${seconds}s`);
      } catch (error) {
        setTimeLeft("");
      }
    };

    updateCountdown();

    const interval = setInterval(updateCountdown, 1000);

    return () => clearInterval(interval);
  }, []);

  if (!timeLeft) return null;

  return (
    <span
      style={{
        marginRight: "15px",
        fontWeight: "bold",
        color: timeLeft === "Expired" ? "red" : "#ff9800",
      }}
    >
      ⏳ {timeLeft}
    </span>
  );
}