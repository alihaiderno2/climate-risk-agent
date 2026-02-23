import React from "react";
import { motion } from "framer-motion";
import { ShieldCheck, Globe, Info, Terminal } from "lucide-react";

const Navbar = () => {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed-top mx-auto mt-3 d-flex align-items-center justify-content-between px-4 py-2"
      style={{
        width: "90%",
        maxWidth: "1000px",
        background: "rgba(255, 255, 255, 0.7)",
        backdropFilter: "blur(12px)",
        borderRadius: "20px",
        border: "1px solid rgba(255, 255, 255, 0.3)",
        zIndex: 1000,
        boxShadow: "0 8px 32px rgba(0, 0, 0, 0.05)",
      }}
    >
      <div className="d-flex align-items-center gap-2">
        <div className="bg-primary rounded-circle p-2 d-flex align-items-center justify-content-center">
          <ShieldCheck size={20} className="text-white" />
        </div>
        <span className="fw-bold text-dark tracking-tight">CLIMATE.AI</span>
      </div>

      <div className="d-none d-md-flex align-items-center gap-4">
        {["Monitor", "Intelligence", "Protocol", "Terminal"].map((item) => (
          <motion.a
            key={item}
            href="#"
            className="text-muted text-decoration-none small fw-bold"
            whileHover={{ color: "#0d6efd", y: -2 }}
          >
            {item}
          </motion.a>
        ))}
      </div>

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="btn btn-dark btn-sm rounded-pill px-3 fw-bold"
      >
        V.2.0 Active
      </motion.button>
    </motion.nav>
  );
};

export default Navbar;
