import React from "react";
import Navbar from "./components/Navbar";
import MainForm from "./components/MainForm";
import FeatureGrid from "./components/FeatureGrid";
import Footer from "./components/Footer";

function App() {
  return (
    // Set a unified background color for the entire page here
    <div
      className="app-container d-flex flex-column"
      style={{
        background: "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)",
        minHeight: "100vh",
      }}
    >
      <Navbar />

      <div style={{ marginTop: "80px" }}>
        <main className="flex-grow-1 d-flex align-items-center justify-content-center py-5">
          <MainForm />
        </main>

        <FeatureGrid />
        <Footer />
      </div>
    </div>
  );
}

export default App;
