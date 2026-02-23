import React from "react";
import { motion } from "framer-motion";
import { Zap, Target, Search } from "lucide-react";

const FeatureGrid = () => {
  const features = [
    {
      icon: <Zap />,
      title: "Real-time Sync",
      desc: "Live OpenWeather API integration.",
    },
    {
      icon: <Target />,
      title: "Persona Risk",
      desc: "Analyzes impact on your specific job.",
    },
    {
      icon: <Search />,
      title: "Deep Analysis",
      desc: "LLM-powered mitigation strategies.",
    },
  ];

  return (
    <div className="container py-5">
      <div className="row g-4">
        {features.map((f, i) => (
          <motion.div
            key={i}
            className="col-md-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.2 }}
          >
            <div className="card h-100 border-0 shadow-sm rounded-4 p-4">
              <div className="text-primary mb-3">{f.icon}</div>
              <h6 className="fw-bold">{f.title}</h6>
              <p className="text-muted small mb-0">{f.desc}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default FeatureGrid;
