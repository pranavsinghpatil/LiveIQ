// src/components/layout/Navbar.tsx
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-gray-800">VoxStitch</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/dashboard" className="text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            <Link to="/login" className="text-gray-600 hover:text-gray-900">
              Login
            </Link>
            <Link to="/register" className="text-gray-600 hover:text-gray-900">
              Register
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
