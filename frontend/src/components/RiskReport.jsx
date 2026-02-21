import React from "react";
import { motion } from "framer-motion";
import {
  Wind,
  Droplets,
  ShieldAlert,
  MapPin,
  Navigation,
  Calendar,
  CheckCircle2,
} from "lucide-react";

const RiskReport = ({ data }) => {
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
        <ShieldAlert size={32} className="me-3 text-danger" />
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
              {data.city_baseline.province}, PK
            </small>
            <div className="mt-2 small text-muted">
              Pop: {data.city_baseline.population.toLocaleString()}
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
                {data.live_weather.temp}°C
              </div>
              <div className="text-end">
                <div className="fw-bold text-capitalize text-dark">
                  {data.live_weather.condition}
                </div>
                <small className="text-muted text-uppercase small">
                  AQI: {data.live_weather.aqi}
                </small>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* FORECAST */}
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
                {new Date(day.date).toLocaleDateString("en-GB", {
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

      {/* SAFETY MEASURES */}
      <motion.div variants={item} className="mb-4">
        <h6 className="fw-bold text-secondary mb-3">
          <CheckCircle2 size={18} className="me-1" /> SAFETY MEASURES
        </h6>
        <div className="row g-3">
          {data.personalized_recommendations.map((rec, idx) => (
            <div key={idx} className="col-12">
              <motion.div
                whileHover={{ x: 5 }}
                className="card border-0 shadow-sm p-3 rounded-4 bg-white text-dark"
              >
                <div className="d-flex align-items-start">
                  <div
                    className={`badge bg-${severityColor} rounded-pill me-3 mt-1`}
                  >
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

      {/* EVACUATION */}
      {data.overall_severity === "High" && data.safe_cities.length > 0 && (
        <motion.div
          variants={item}
          className="card border-0 shadow-lg rounded-4 bg-dark text-white p-4"
        >
          <div className="d-flex align-items-center mb-2 text-warning">
            <Navigation size={20} className="me-2" />
            <h5 className="mb-0 fw-bold">EVACUATION PLAN</h5>
          </div>
          <p className="small text-light opacity-75">
            {data.safe_cities[0].plan}
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default RiskReport;
