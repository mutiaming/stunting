import React, { useState } from "react";
import { Form, Button, Container, Card, Alert } from "react-bootstrap";
import { useNavigate, Link } from "react-router-dom";

import Navbar from "./Navbar";
import "../App.css";

const About = () => {
  return (
    <>
    {/* 🏠 Navbar */}
      <Navbar />
    <section className="about-section" style={{ padding: "80px 0", backgroundColor: "#f8f9fa" }}>
      <div className="container" style={{ maxWidth: "900px", margin: "0 auto", textAlign: "center" }}>
        <h2 style={{ fontSize: "2.5rem", fontWeight: "700", color: "#007bff", marginBottom: "20px" }}>
          Tentang GrowTrack
        </h2>
        <p style={{ fontSize: "1.1rem", color: "#555", lineHeight: "1.8" }}>
          <strong>GrowTrack</strong> adalah platform berbasis web yang dirancang untuk membantu
          orang tua, tenaga kesehatan, dan peneliti dalam memantau serta mengelola
          pertumbuhan dan perkembangan anak. Kami menggabungkan data kesehatan dengan
          teknologi analitik modern untuk memberikan wawasan yang akurat dan mudah dipahami.
        </p>

        <div style={{ marginTop: "50px" }}>
          <h3 style={{ color: "#333", fontSize: "1.8rem", marginBottom: "15px" }}>Visi Kami</h3>
          <p style={{ fontSize: "1.05rem", color: "#555", lineHeight: "1.8" }}>
            Menjadi solusi digital terpercaya dalam pemantauan tumbuh kembang anak
            dengan pendekatan ilmiah dan berkelanjutan.
          </p>
        </div>

        <div style={{ marginTop: "40px" }}>
          <h3 style={{ color: "#333", fontSize: "1.8rem", marginBottom: "15px" }}>Misi Kami</h3>
          <ul style={{ listStyle: "none", padding: 0, color: "#555", fontSize: "1.05rem", lineHeight: "1.8" }}>
            <li>✅ Menyediakan data pertumbuhan yang akurat dan mudah diakses.</li>
            <li>✅ Mendukung edukasi gizi dan kesehatan anak sejak dini.</li>
            <li>✅ Mendorong kolaborasi antara keluarga dan tenaga medis.</li>
          </ul>
        </div>

        <div style={{ marginTop: "60px", backgroundColor: "#fff", padding: "30px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.1)" }}>
          <h3 style={{ color: "#007bff", marginBottom: "15px" }}>Tim Kami</h3>
          <p style={{ color: "#555" }}>
            Tim GrowTrack terdiri dari para profesional di bidang teknologi informasi,
            kesehatan masyarakat, dan gizi anak yang memiliki visi yang sama:
            menciptakan generasi yang tumbuh optimal melalui teknologi cerdas.
          </p>
        </div>
      </div>
    </section>
    </>
  );
};

export default About;


