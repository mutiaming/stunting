import React, { useEffect, useState } from "react";
import { Table, Container, Navbar, Form, FormControl, Alert } from "react-bootstrap";
import Sidebar from "./Sidebar"; // Import Sidebar dinamis

const IbuHistory = () => {
  const [prediksiList, setPrediksiList] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState("");
  const [role, setRole] = useState(""); // State untuk role pengguna

  useEffect(() => {
    const fetchPrediksi = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/ibu/history", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });

        const data = await response.json();
        console.log("Data fetched:", data); // Debugging

        if (response.ok) {
          setPrediksiList(data.predictions || data.data || []);
        } else {
          setError(data.error || "Gagal mengambil data.");
        }
      } catch (error) {
        console.error("Gagal mengambil data prediksi:", error);
        setError("Terjadi kesalahan saat mengambil data.");
      }
    };

    const fetchUserRole = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/auth/profile", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        const data = await response.json();
        setRole(data.role); // Set role pengguna
      } catch (error) {
        console.error("Gagal mengambil role pengguna:", error);
      }
    };

    fetchPrediksi();
    fetchUserRole();
  }, []);

  const filteredPrediksi = prediksiList.filter((item) =>
    item.username.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="d-flex">
      <Sidebar role={role} /> {/* Gunakan Sidebar dinamis dan kirim role sebagai prop */}
      <Container className="mt-4">
        <Navbar bg="light" expand="lg" className="mb-3 p-3 d-flex justify-content-between">
          <Navbar.Brand>Riwayat Prediksi Calon Ibu</Navbar.Brand>
          <Form className="d-flex">
            <FormControl
              type="text"
              placeholder="Cari berdasarkan Username..."
              className="me-2"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </Form>
        </Navbar>

        {error && <Alert variant="danger">{error}</Alert>}

        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>No</th>
              <th>Username</th>
              <th>Usia</th>
              <th>BB (kg)</th>
              <th>TB (cm)</th>
              <th>Hasil Prediksi</th>
              <th>Tanggal</th>
            </tr>
          </thead>
          <tbody>
            {filteredPrediksi.length > 0 ? (
              filteredPrediksi.map((item, index) => (
                <tr key={item.id}>
                  <td>{index + 1}</td>
                  <td>{item.username}</td>
                  <td>{item.usia}</td>
                  <td>{item.berat_badan || "N/A"}</td>
                  <td>{item.tinggi_badan || "N/A"}</td>
                  <td>{item.hasil_prediksi}</td>
                  <td>
                    {item.created_at
                      ? new Date(item.created_at).toLocaleString("id-ID")
                      : "Tanggal tidak tersedia"}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="text-center">
                  {searchTerm ? "Data tidak ditemukan" : "Belum ada data prediksi"}
                </td>
              </tr>
            )}
          </tbody>
        </Table>
      </Container>
    </div>
  );
};

export default IbuHistory;