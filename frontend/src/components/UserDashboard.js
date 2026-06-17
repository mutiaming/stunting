// 📂 /src/components/BidanDashboard.js
import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import SideUser from "./SideUser";

const UserDashboard = () => {
  return (
    <div className="vh-100 d-flex flex-column">
      <Navbar />
      <div className="d-flex">
        {/* 🔹 Sidebar Tetap Ada */}
        <SideUser />
        {/* 🔹 Halaman Berubah di Sini */}
        <div className="flex-grow-1 p-4">
            <div className="welcome-message">
             <h1>Selamat Datang di Dashboard User</h1>
             <p>Anda dapat mengelola semua fitur aplikasi dari sini.</p>
            </div>
           <Outlet />
       </div>
      </div>
    </div>
  );
};

export default UserDashboard;
