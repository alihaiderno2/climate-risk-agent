import React from "react";

const Footer = () => {
  return (
    <footer className="py-5 bg-white border-top mt-auto">
      <div className="container text-center">
        <p className="text-muted small mb-0">
          © 2026 Climate Risk Agent Portal. Designed for
          <span className="text-primary fw-bold"> Gen AI </span>.
        </p>
        <div className="d-flex justify-content-center gap-3 mt-3">
          <div className="d-flex align-items-center gap-1 small text-muted">
            <div
              className="bg-success rounded-circle"
              style={{ width: "8px", height: "8px" }}
            ></div>
            All Systems Operational
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
