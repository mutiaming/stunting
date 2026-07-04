import { useParams } from "react-router-dom";
import React, { useEffect, useState } from "react";
import { Container, Form, Button } from "react-bootstrap";
import Sidebar from "../components/Sidebar";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";
const GrafikPertumbuhan = () => {
  const [role, setRole] = useState("");
  const [chartData, setChartData] = useState([]);
  const { nik } = useParams();

  
  const [bulan, setBulan] = useState(
    new Date().toISOString().slice(0, 7)
  );

  useEffect(() => {
    fetch("https://api.growtrack.harkatnegeri.ac.id/auth/profile", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })
      .then(res => res.json())
      .then(data => setRole(data.role));
  }, []);

  useEffect(() => {
    loadChart();
  }, [bulan, nik]);

  const loadChart = async () => {
    if (!nik || !bulan) {
      alert("Masukkan NIK dan Bulan");
      return;
    }
    try {
      const response = await fetch(
        `https://api.growtrack.harkatnegeri.ac.id/stunting/chart/${nik}?month=${bulan}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        }
      );
      const data = await response.json();
      setChartData(data.chart);
    } catch (err) {
      console.log(err);
    }
  }
  return (
    <div className="d-flex">
      <Sidebar role={role} />
      <Container className="mt-4">
        <h3>Grafik Perkembangan Anak</h3>
        <Form className="mb-4">
          <Form.Group>
            <Form.Label>Bulan</Form.Label>
            <Form.Control
              type="month"
              value={bulan}
              onChange={(e) => setBulan(e.target.value)}
            />
          </Form.Group>
        </Form>
        {/* GRAFIK DIMULAI DI SINI */}
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="tanggal" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="linear"
              dataKey="berat_badan"
              name="Berat Badan (kg)"
              stroke="#2563EB"
              strokeWidth={3}
              dot={{ fill: "#2563EB", r: 5 }}
            />
            <Line
              type="linear"
              dataKey="tinggi_badan"
              name="Tinggi Badan (cm)"
              stroke="#16A34A"
              strokeWidth={3}
              dot={{ fill: "#16A34A", r: 5 }}
            />
            <Line
              type="linear"
              dataKey="z_score"
              name="Z-Score"
              stroke="#DC2626"
              strokeWidth={3}
              dot={{ fill: "#DC2626", r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
        {/* GRAFIK SELESAI */}
      </Container>
    </div>
  )
}
export default GrafikPertumbuhan;