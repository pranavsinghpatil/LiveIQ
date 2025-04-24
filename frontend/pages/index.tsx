import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import api from "../services/api";
import { useAuthStore } from "../store/auth";

export default function LoginPage() {
  const router = useRouter();
  const [identifier, setIdentifier] = useState(""); // username or email
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { token, setToken } = useAuthStore();

  useEffect(() => {
    if (token) {
      router.replace("/dashboard");
    }
  }, [token, router]);

  const handleLogin = async () => {
    try {
      const params = new URLSearchParams();
      params.append("username", identifier);
      params.append("password", password);
      const res = await api.post("/api/auth/token", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      localStorage.setItem("access_token", res.data.access_token);
      setToken(res.data.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError("Invalid credentials. Try again.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">VoxStitch Login</h1>
      <input
        type="text"
        placeholder="Username or Email"
        className="p-2 border w-64 mb-2"
        value={identifier}
        onChange={(e) => setIdentifier(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="p-2 border w-64 mb-4"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin} className="bg-blue-600 text-white px-4 py-2 rounded">
        Login
      </button>
      {error && <p className="text-red-600 mt-4">{error}</p>}
      <button
        className="mt-4 text-blue-700 underline hover:text-blue-900"
        onClick={() => router.push("/register")}
      >
        New user? Register here
      </button>
    </div>
  );
}
