// src/pages/NotFound.tsx
import { useNavigate } from "react-router-dom";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-primary">404</h1>
        <p className="mt-4 text-xl text-text">Page not found</p>
        <p className="mt-2 text-text/60">The page you're looking for doesn't exist.</p>
        <button
          onClick={() => navigate("/")}
          className="mt-6 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark transition-colors"
        >
          Go Home
        </button>
      </div>
    </div>
  );
}
