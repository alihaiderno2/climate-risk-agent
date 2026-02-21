import React, { useState } from "react";

const MainForm = () => {
  // Cities list from your Pakistan dataset
  const pkCities = [
    "Karachi",
    "Lahore",
    "Sialkot",
    "Faisalabad",
    "Rawalpindi",
    "Peshawar",
    "Multan",
    "Gujranwala",
    "Islamabad",
    "Quetta",
    "Bahawalpur",
  ];

  // Professional categories for personalized safety
  const professionSuggestions = [
    "Farmer",
    "Student",
    "Healthcare Worker",
    "Outdoor Worker",
    "Businessperson",
    "General Citizen",
  ];

  // Core climate risks
  const riskSuggestions = ["Flood", "Drought", "Heatwave", "Air Quality"];

  const [formData, setFormData] = useState({
    city: "",
    profession: "",
    concern: "",
  });

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-6 col-md-8">
          <div className="card border-0 shadow-lg rounded-5 overflow-hidden">
            {/* Top Interactive Banner */}
            <div className="bg-primary p-4 text-white text-center">
              <h3 className="fw-bold mb-0">Agentic Climate Risk System</h3>
              <p className="small opacity-75 mb-0">
                Pakistan Region Monitoring
              </p>
            </div>

            <div className="card-body p-4 p-md-5">
              <form>
                {/* 1. City Input with Search Dropdown */}
                <div className="mb-4">
                  <label className="form-label fw-bold text-secondary">
                    Location (City)
                  </label>
                  <input
                    className="form-control form-control-lg border-2 shadow-sm"
                    list="cityOptions"
                    name="city"
                    placeholder="Type to search city..."
                    onChange={handleChange}
                  />
                  <datalist id="cityOptions">
                    {pkCities.map((city) => (
                      <option key={city} value={city} />
                    ))}
                  </datalist>
                </div>

                {/* 2. Profession Input with Suggestions */}
                <div className="mb-4">
                  <label className="form-label fw-bold text-secondary">
                    Profession / Role
                  </label>
                  <input
                    className="form-control form-control-lg border-2 shadow-sm"
                    list="professionOptions"
                    name="profession"
                    placeholder="e.g. Farmer, Student..."
                    onChange={handleChange}
                  />
                  <datalist id="professionOptions">
                    {professionSuggestions.map((p) => (
                      <option key={p} value={p} />
                    ))}
                  </datalist>
                </div>

                {/* 3. Concern Input with Suggestions */}
                <div className="mb-4">
                  <label className="form-label fw-bold text-secondary">
                    Climate Concern
                  </label>
                  <input
                    className="form-control form-control-lg border-2 shadow-sm"
                    list="riskOptions"
                    name="concern"
                    placeholder="e.g. Heatwave, Flood..."
                    onChange={handleChange}
                  />
                  <datalist id="riskOptions">
                    {riskSuggestions.map((r) => (
                      <option key={r} value={r} />
                    ))}
                  </datalist>
                </div>

                {/* Interactive Action Button */}
                <button
                  type="button"
                  className="btn btn-primary btn-lg w-100 rounded-pill fw-bold shadow mt-3 py-3 transition-all"
                >
                  Generate Risk Report →
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainForm;
