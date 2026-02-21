import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sun, Cloud, CloudRain, Zap } from "lucide-react";

const ClimateLoader = ({ loading, progress, loaderIndex }) => {
  const loaderIcons = [
    {
      icon: <Sun size={60} className="text-warning mb-3" />,
      text: "Syncing Live Weather...",
    },
    {
      icon: <Cloud size={60} className="text-secondary mb-3" />,
      text: "Analyzing Atmosphere...",
    },
    {
      icon: <CloudRain size={60} className="text-info mb-3" />,
      text: "Simulating Risks...",
    },
    {
      icon: <Zap size={60} className="text-danger mb-3" />,
      text: "Generating Report...",
    },
  ];

  return (
    <AnimatePresence>
      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="position-fixed top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center"
          style={{
            background: "rgba(255, 255, 255, 0.98)",
            backdropFilter: "blur(15px)",
            zIndex: 3000,
          }}
        >
          <motion.div
            key={loaderIndex}
            initial={{ scale: 0.8, opacity: 0, y: 10 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 1.1, opacity: 0, y: -10 }}
            className="text-center"
          >
            {loaderIcons[loaderIndex].icon}
            <h4 className="fw-bold text-dark">
              {loaderIcons[loaderIndex].text}
            </h4>
          </motion.div>

          <div className="mt-4" style={{ width: "280px" }}>
            <div
              className="progress rounded-pill bg-light border-0 shadow-sm"
              style={{ height: "10px" }}
            >
              <motion.div
                className="progress-bar progress-bar-striped progress-bar-animated bg-primary"
                initial={{ width: "0%" }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.4 }}
              ></motion.div>
            </div>
            <div className="text-center mt-2 small fw-bold text-primary">
              AGENT ANALYSIS: {progress}%
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ClimateLoader;
