import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  MapPin,
  Briefcase,
  AlertTriangle,
  ChevronRight,
  Activity,
  X,
  ShieldCheck,
} from "lucide-react";
import RiskReport from "./RiskReport";
import ClimateLoader from "./ClimateLoader";
import "./MainForm.css";

const MainForm = () => {
  const [formData, setFormData] = useState({
    city: "",
    profession: "",
    concern: "",
  });
  const [reportData, setReportData] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loaderIndex, setLoaderIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  const pkCities = [
    "Karachi",
    "Lahore",
    "Sialkot",
    "Faisalabad",
    "Rawalpindi",
    "Peshawar",
    "Islamabad",
    "Quetta",
  ];
  const professionSuggestions = [
    "Farmer",
    "Student",
    "Healthcare Worker",
    "Outdoor Worker",
    "Businessperson",
    "General Citizen",
  ];
  const riskSuggestions = ["Flood", "Drought", "Heatwave", "Air Quality"];

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setLoaderIndex((prev) => (prev + 1) % 4);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setProgress(20);
    try {
      setTimeout(() => setProgress(50), 400);
      const response = await fetch("https://climate-risk-api.onrender.com/api/analyze-risk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          city: formData.city.toLowerCase(),
          profession: formData.profession.toLowerCase(),
          concern: formData.concern.toLowerCase(),
        }),
      });
      setProgress(85);
      const data = await response.json();
      setProgress(100);
      setTimeout(() => {
        setReportData(data);
        setLoading(false);
        setShowModal(true);
      }, 600);
    } catch (error) {
      setLoading(false);
      alert("System Error: " + error.message);
    }
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center p-4 bg-dashboard">
      <ClimateLoader
        loading={loading}
        progress={progress}
        loaderIndex={loaderIndex}
      />

      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        className="card border-0 shadow-2xl rounded-5 overflow-hidden glass-card"
        style={{
          maxWidth: "480px",
          width: "100%",
          display: loading ? "none" : "block",
        }}
      >
        <div className="bg-gradient-primary p-5 text-center text-white">
          <ShieldCheck size={42} className="mb-3 opacity-90" />
          <h3 className="fw-bold mb-1">Climate Intelligence</h3>
          <p className="small opacity-80 mb-0 text-uppercase">
            Regional Risk Monitoring
          </p>
        </div>

        <div className="card-body p-5">
          <form onSubmit={handleSubmit} className="floating-form">
            <div className="form-group position-relative mb-4">
              <input
                type="text"
                name="city"
                className="floating-input"
                placeholder=" "
                list="cities"
                onChange={handleChange}
                required
                autoComplete="off"
              />
              <label className="floating-label d-flex align-items-center">
                <MapPin size={14} className="me-2" />
                Target City
              </label>
              <datalist id="cities">
                {pkCities.map((c) => (
                  <option key={c} value={c} />
                ))}
              </datalist>
            </div>

            <div className="form-group position-relative mb-4">
              <input
                type="text"
                name="profession"
                className="floating-input"
                placeholder=" "
                list="profs"
                onChange={handleChange}
                required
                autoComplete="off"
              />
              <label className="floating-label d-flex align-items-center">
                <Briefcase size={14} className="me-2" />
                Your Profession
              </label>
              <datalist id="profs">
                {professionSuggestions.map((p) => (
                  <option key={p} value={p} />
                ))}
              </datalist>
            </div>

            <div className="form-group position-relative mb-5">
              <input
                type="text"
                name="concern"
                className="floating-input"
                placeholder=" "
                list="risks"
                onChange={handleChange}
                required
                autoComplete="off"
              />
              <label className="floating-label d-flex align-items-center">
                <AlertTriangle size={14} className="me-2" />
                Primary Concern
              </label>
              <datalist id="risks">
                {riskSuggestions.map((r) => (
                  <option key={r} value={r} />
                ))}
              </datalist>
            </div>

            <motion.button
              whileHover={{
                y: -2,
                boxShadow: "0 10px 20px rgba(13, 110, 253, 0.3)",
              }}
              whileTap={{ scale: 0.98 }}
              className="btn btn-primary btn-lg w-100 rounded-pill py-3 fw-bold border-0 shadow-lg text-uppercase tracking-wider"
            >
              Initiate Intelligence Scan{" "}
              <ChevronRight size={18} className="ms-1" />
            </motion.button>
          </form>
        </div>
      </motion.div>

      <AnimatePresence>
        {showModal && reportData && (
          <motion.div
            className="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center p-3"
            style={{
              background: "rgba(15, 23, 42, 0.75)",
              backdropFilter: "blur(12px)",
              zIndex: 2000,
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="bg-white rounded-5 shadow-2xl w-100 overflow-hidden"
              style={{ maxWidth: "820px", maxHeight: "85vh" }}
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
            >
              <div className="p-4 border-bottom d-flex justify-content-between align-items-center bg-white sticky-top">
                <h6 className="mb-0 fw-bold text-primary tracking-widest text-uppercase">
                  Result for {formData.city}
                </h6>
                <motion.button
                  className="btn border-0 d-flex align-items-center justify-content-center"
                  style={{
                    background: "#f8f9fa",
                    width: "40px",
                    height: "40px",
                    borderRadius: "12px",
                    color: "#dc3545",
                  }}
                  whileHover={{
                    rotate: 90,
                    scale: 1.1,
                    backgroundColor: "#dc3545",
                    color: "#fff",
                  }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setShowModal(false)}
                >
                  <X size={24} strokeWidth={2.5} />
                </motion.button>
              </div>
              <div
                className="overflow-auto"
                style={{ maxHeight: "calc(85vh - 75px)" }}
              >
                <RiskReport data={reportData} />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default MainForm;
