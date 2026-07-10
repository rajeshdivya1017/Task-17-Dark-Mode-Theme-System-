import { useEffect, useState } from "react";
import api from "../../api";
import { useParams, useNavigate } from "react-router-dom";
import { useToast } from "../../hooks/useToast";

export default function ProductForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toasts, showToast } = useToast();

  const isEdit = Boolean(id);

  const [data, setData] = useState({
    name: "",
    description: "",
    price: "",
    stock: "",
    category_id: "",
    image_url: ""
  });

  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState("");

  useEffect(() => {
    if (isEdit) {
      api.get(`/api/products/${id}`).then((res) => {
        const p = res.data;

        setData({
          name: p.name || "",
          description: p.description || "",
          price: p.price || "",
          stock: p.stock || "",
          category_id: p.category_id || "",
          image_url: p.image_url || ""
        });

        if (p.image_url) {
          setPreview(`http://localhost:5000${p.image_url}`);
        }
      });
    }
  }, [id]);

  const handleChange = (e) => {
    setData({
      ...data,
      [e.target.name]: e.target.value
    });
  };

  const handleImage = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setImageFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const uploadImage = async () => {
  if (!imageFile) return data.image_url;

  try {
    const formData = new FormData();
    formData.append("image", imageFile);

    const res = await api.post("/api/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    showToast("Image uploaded successfully!", "success");
    return res.data.image_url;

  } catch (err) {
    showToast("Image upload failed!", "error");
    throw err;
  }
};

  const submit = async () => {
    try {
      const image_url = await uploadImage();

      const payload = {
        ...data,
        image_url
      };

      if (isEdit) {
        await api.put(`/api/products/${id}`, payload);
      } else {
        await api.post("/api/products", payload);
      }

      showToast(
  isEdit
    ? "Product updated successfully!"
    : "Product added successfully!",
  "success"
);

setTimeout(() => {
  navigate("/admin/products");
}, 1000);

    } catch (err) {
      console.error(err);
      showToast("Error saving product!", "error");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "500px" }}>
      <div
  style={{
    position: "fixed",
    top: 20,
    right: 20,
    zIndex: 9999,
  }}
>
  {toasts.map((toast) => (
    <div
      key={toast.id}
      style={{
        marginBottom: "10px",
        padding: "12px 18px",
        borderRadius: "8px",
        color: "#fff",
        background:
          toast.type === "success"
            ? "#28a745"
            : toast.type === "error"
            ? "#dc3545"
            : toast.type === "warning"
            ? "#ffc107"
            : "#0d6efd",
      }}
    >
      {toast.message}
    </div>
  ))}
</div>
      <h2>{isEdit ? "Edit Product" : "Add Product"}</h2>

      <input
        name="name"
        placeholder="Name"
        value={data.name}
        onChange={handleChange}
      />

      <textarea
        name="description"
        placeholder="Description"
        value={data.description}
        onChange={handleChange}
      />

      <input
        type="number"
        name="price"
        placeholder="Price"
        value={data.price}
        onChange={handleChange}
      />

      <input
        type="number"
        name="stock"
        placeholder="Stock"
        value={data.stock}
        onChange={handleChange}
      />

      <input
        type="number"
        name="category_id"
        placeholder="Category ID"
        value={data.category_id}
        onChange={handleChange}
      />

      <label>Select Image</label>

      <input
        type="file"
        accept="image/*"
        onChange={handleImage}
      />

      {preview ? (
        <img
          src={preview}
          alt="Preview"
          style={{
            width: "180px",
            height: "180px",
            objectFit: "cover",
            marginTop: "10px",
            borderRadius: "8px"
          }}
        />
      ) : (
        <p>No Image Selected</p>
      )}

      <br />

      <button onClick={submit}>
        {isEdit ? "Update Product" : "Add Product"}
      </button>
    </div>
  );
}