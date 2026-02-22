import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Wind,
  ShieldAlert,
  MapPin,
  Navigation,
  Calendar,
  CheckCircle2,
  Package,
  Send,
  Radio
} from "lucide-react";

const RiskReport = ({ data }) => {
  const [emailStatus, setEmailStatus] = useState("");

  if (!data) return null;

  const severityColor = data.overall_severity === "High" ? "danger" : "warning";

  const container = {
    hidden: { opacity: 0 },
    show: { opacity: 1, transition: { staggerChildren: 0.1 } },
  };

  const item = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1 },
  };

  const handleSendEmail = async () => {
    setEmailStatus("sending");
    try {
      const response = await fetch("https://climate-risk-api.onrender.com/api/send-alert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dispatch_text: data.official_dispatch,
          logistics: data.relief_logistics || {},
          // Change this to whatever email you want to show the judges!
          recipient_email: "alihaiderno2@gmail.com", 
        }),
      });
      
      if (response.ok) {
        setEmailStatus("success");
      } else {
        setEmailStatus("error");
      }
    } catch (error) {
      setEmailStatus("error");
    }
  };

  return (
    <motion.div
      className="p-4 bg-light overflow-hidden text-start"
      variants={container}
      initial="hidden"
      animate="show"
    >
      {/* SEVERITY */}
      <motion.div
        variants={item}
        className={`alert alert-${severityColor} border-0 rounded-4 shadow-sm d-flex align-items-center p-3 mb-4 text-dark`}
      >
        <ShieldAlert size={32} className={`me-3 text-${severityColor}`} />
        <div>
          <h4 className="mb-0 fw-bold">
            Overall Severity: {data.overall_severity}
          </h4>
          <small className="opacity-75 text-capitalize">
            Personalized for a {data.profession} in {data.city}
          </small>
        </div>
      </motion.div>

      {/* WEATHER GRID */}
      <div className="row g-3 mb-4">
        <motion.div variants={item} className="col-md-4">
          <div className="card border-0 shadow-sm rounded-4 p-3 h-100 bg-white">
            <div className="text-primary mb-2">
              <MapPin size={20} /> <small className="fw-bold">LOCATION</small>
            </div>
            <h5 className="mb-0 text-capitalize">{data.city}</h5>
            <small className="text-muted">
              {data.city_baseline?.province || "Pakistan"}
            </small>
            <div className="mt-2 small text-muted">
              Pop: {data.city_baseline?.population?.toLocaleString() || "N/A"}
            </div>
          </div>
        </motion.div>

        <motion.div variants={item} className="col-md-8">
          <div className="card border-0 shadow-sm rounded-4 p-3 h-100 bg-white">
            <div className="text-info mb-2">
              <Wind size={20} /> <small className="fw-bold">LIVE WEATHER</small>
            </div>
            <div className="d-flex justify-content-between align-items-center">
              <div className="h3 mb-0 fw-bold text-dark">
                {data.live_weather?.temp}°C
              </div>
              <div className="text-end">
                <div className="fw-bold text-capitalize text-dark">
                  {data.live_weather?.condition}
                </div>
                <small className="text-muted text-uppercase small">
                  AQI: {data.live_weather?.aqi}
                </small>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* FORECAST */}
      {data.forecast_weather?.length > 0 && (
        <motion.div variants={item} className="mb-4">
          <h6 className="fw-bold text-secondary mb-3">
            <Calendar size={18} className="me-1" /> 3-DAY FORECAST
          </h6>
          <div className="d-flex gap-3 overflow-auto pb-2 scrollbar-hidden">
            {data.forecast_weather.map((day, idx) => (
              <div
                key={idx}
                className="bg-white p-3 rounded-4 shadow-sm text-center border-0 text-dark"
                style={{ minWidth: "140px" }}
              >
                <div className="small text-muted mb-1">
                  {day.date === "Tomorrow" ? "Tomorrow" : new Date(day.date).toLocaleDateString("en-GB", {
                    weekday: "short",
                    day: "numeric",
                  })}
                </div>
                <div className="fw-bold text-primary">{day.max_temp}°</div>
                <div className="small text-muted">{day.min_temp}°</div>
                <div className="small mt-1 text-truncate opacity-75">
                  {day.condition}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* SAFETY MEASURES & SURVIVAL KIT */}
      <div className="row g-3 mb-4">
        {/* Left Col: Advice */}
        <motion.div variants={item} className="col-md-7">
          <h6 className="fw-bold text-secondary mb-3">
            <CheckCircle2 size={18} className="me-1" /> SAFETY MEASURES
          </h6>
          <div className="row g-3">
            {data.personalized_recommendations?.map((rec, idx) => (
              <div key={idx} className="col-12">
                <motion.div
                  whileHover={{ x: 5 }}
                  className="card border-0 shadow-sm p-3 rounded-4 bg-white text-dark h-100"
                >
                  <div className="d-flex align-items-start">
                    <div className={`badge bg-${severityColor} rounded-pill me-3 mt-1`}>
                      {idx + 1}
                    </div>
                    <p className="mb-0 small fw-medium">
                      {rec.replace("• ", "")}
                    </p>
                  </div>
                </motion.div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Right Col: Kit */}
        {data.survival_kit && (
          <motion.div variants={item} className="col-md-5">
            <h6 className="fw-bold text-secondary mb-3">
              <Package size={18} className="me-1" /> SURVIVAL KIT
            </h6>
            <div className="card border-0 shadow-sm p-3 rounded-4 bg-white text-dark h-100">
              <ul className="list-unstyled mb-0">
                {data.survival_kit.map((kitItem, idx) => (
                  <li key={idx} className="mb-2 small d-flex align-items-start">
                    <input type="checkbox" className="form-check-input me-2 mt-1" />
                    <span className="fw-medium">{kitItem.replace("• ", "")}</span>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}
      </div>

      {/* EVACUATION & PDMA ALERTS (Only show if High Risk) */}
      {data.overall_severity === "High" && (
        <motion.div variants={item} className="row g-3">
          
          {/* Evacuation Route */}
          {data.safe_cities?.length > 0 && (
            <div className="col-12">
              <div className="card border-0 shadow-sm rounded-4 bg-dark text-white p-4">
                <div className="d-flex align-items-center mb-2 text-warning">
                  <Navigation size={20} className="me-2" />
                  <h5 className="mb-0 fw-bold">EVACUATION PLAN</h5>
                </div>
                <p className="small text-light opacity-75 mb-0">
                  {data.safe_cities[0].plan}
                </p>
              </div>
            </div>
          )}

          {/* PDMA SitRep Dashboard */}
          {data.official_dispatch && (
            <div className="col-12">
              <div className="card border-0 shadow-sm rounded-4 p-4" style={{ backgroundColor: "#0f172a", color: "#e2e8f0" }}>
                <div className="d-flex justify-content-between align-items-center border-bottom border-secondary pb-2 mb-3">
                  <div className="d-flex align-items-center text-success">
                    <Radio size={20} className="me-2" />
                    <h5 className="mb-0 fw-bold font-monospace">PDMA SITREP TERMINAL</h5>
                  </div>
                  <span className="badge bg-danger">CLASSIFIED</span>
                </div>
                
                <p className="small font-monospace opacity-75 mb-4 lh-lg">
                  {data.official_dispatch}
                </p>

                <div className="row g-2 mb-4 font-monospace text-center">
                  <div className="col-4">
                    <div className="bg-dark p-2 rounded border border-secondary">
                      <div className="small text-info">WATER (L)</div>
                      <div className="fw-bold">{data.relief_logistics?.water_liters?.toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="col-4">
                    <div className="bg-dark p-2 rounded border border-secondary">
                      <div className="small text-warning">TENTS</div>
                      <div className="fw-bold">{data.relief_logistics?.tents?.toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="col-4">
                    <div className="bg-dark p-2 rounded border border-secondary">
                      <div className="small text-danger">MED KITS</div>
                      <div className="fw-bold">{data.relief_logistics?.medical_kits?.toLocaleString()}</div>
                    </div>
                  </div>
                </div>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleSendEmail}
                  disabled={emailStatus === "sending" || emailStatus === "success"}
                  className={`btn w-100 fw-bold py-3 d-flex justify-content-center align-items-center ${
                    emailStatus === "success" ? "btn-success" : "btn-danger"
                  }`}
                >
                  {emailStatus === "" && <><Send size={18} className="me-2" /> DISPATCH ALERT TO NGO</>}
                  {emailStatus === "sending" && "TRANSMITTING..."}
                  {emailStatus === "success" && " ALERT TRANSMITTED"}
                  {emailStatus === "error" && " TRANSMISSION FAILED - RETRY"}
                </motion.button>
              </div>
            </div>
          )}
        </motion.div>
      )}

    </motion.div>
  );
};

export default RiskReport;