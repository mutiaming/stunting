import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Container, Navbar as BootstrapNavbar, Nav } from "react-bootstrap";
import "../App.css";

const CustomNavbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = !!localStorage.getItem("token"); // Cek apakah user sudah login

  const handleLogout = () => {
    localStorage.removeItem("token"); // Hapus token dari localStorage
    navigate("/login"); // Arahkan ke halaman login
  };

  return (
    <div style={{ margin: 0, padding: 0 }}>
      {/* Navbar */}
      <BootstrapNavbar bg="primary" variant="dark" expand="lg">
        <Container>
          <BootstrapNavbar.Brand onClick={() => navigate("/")} style={{ cursor: "pointer" }}>
            GROWTRACK
          </BootstrapNavbar.Brand>
        </Container>
      </BootstrapNavbar>

      {/* Gambar full layar */}
      <img
        src="/Picture1.png"
        alt="Prediksi Stunting"
        style={{
          width: "100vw",
          height: "auto",
          display: "block",
          objectFit: "cover",
          margin: 0,
          padding: 0,
        }}
      />

      {/* Tabs Navigasi */}
      <div className="navbar-tabs-container">
        <Nav className="justify-content-center navbar-tabs">
          <Nav.Link
            onClick={() => navigate("/")}
            className={`tab-link ${location.pathname === "/" ? "active-tab" : ""}`}
          >
            Home
          </Nav.Link>
          <Nav.Link
            onClick={() => navigate("/mpasi")}
            className={`tab-link ${location.pathname === "/mpasi" ? "active-tab" : ""}`}
          >
            MPASI
          </Nav.Link>
          {/* <Nav.Link
            onClick={() => navigate("/ibu_prediction")}
            className={`tab-link ${location.pathname === "/ibu_prediction" ? "active-tab" : ""}`}
          >
            Prediksi calon ibu
          </Nav.Link> */}
          {isAuthenticated ? (
            <Nav.Link onClick={handleLogout} className="tab-link">Logout</Nav.Link>
          ) : (
            <Nav.Link
              onClick={() => navigate("/login")}
              className={`tab-link ${location.pathname === "/login" ? "active-tab" : ""}`}
            >
              Login
            </Nav.Link>
          )}
          <Nav.Link
            onClick={() => navigate("/About")}
            className={`tab-link ${location.pathname === "/About" ? "active-tab" : ""}`}
          >
            About
          </Nav.Link>
        </Nav>
      </div>
    </div>
  );
};

export default CustomNavbar;
