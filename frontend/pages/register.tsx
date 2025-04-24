import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import api from "../services/api";
import { useAuthStore } from "../store/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { token, setToken } = useAuthStore();

  useEffect(() => {
    if (token) {
      router.replace("/dashboard");
    }
  }, [token, router]);

  const handleRegister = async () => {
    try {
      await api.post("/auth/register", { username, email, password });
      // Auto-login after successful registration
      const loginRes = await api.post("/auth/token", {
        username: email || username, // Try email first, fallback to username
        password,
      });
      localStorage.setItem("access_token", loginRes.data.access_token);
      setToken(loginRes.data.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError("Registration failed.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Create a VoxStitch Account</h1>
      <input
        type="text"
        placeholder="Username"
        className="p-2 border w-64 mb-2"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        className="p-2 border w-64 mb-2"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="p-2 border w-64 mb-4"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleRegister} className="bg-green-600 text-white px-4 py-2 rounded">
        Register
      </button>
      {error && <p className="text-red-600 mt-4">{error}</p>}
    </div>
  );
}
