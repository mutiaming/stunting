import React, { useState, useEffect } from "react";
import { Form, Button, Container, Row, Col, ProgressBar, Alert, Card, Navbar,ListGroup} from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import SideBidan from "./SideBidan";

const StuntingPrediction = () => {
  // Form data state
  const [formData, setFormData] = useState({
    id_anak: "",
    nik: "",
    nama_anak: "",
    nama_orang_tua: "",
    jenis_kelamin: "",
    umur: "",
    tinggi_badan: "",
    berat_badan: "",
  });

  // App state
  const [anakList, setAnakList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [apiResponse, setApiResponse] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  // Constants
  const STUNTING_THRESHOLD = -2;
  const stuntingRecommendations = [
    "Memberikan ASI eksklusif hingga bayi berusia 6 bulan",
    "Memberikan MPASI yang bergizi dan kaya protein hewani untuk bayi yang berusia di atas 6 bulan",
    "Memantau perkembangan anak dan membawa ke posyandu secara berkala",
    "Mengonsumsi secara rutin Tablet Tambah Darah (TTD)",
    "Melakukan imunisasi rutin",
    "Memantau tumbuh kembang anak",
    "Menerapkan perilaku hidup bersih dan sehat",
    "Memakai jamban sehat",
    "Konsultasikan dengan dokter atau ahli gizi",
    "Pertahankan gizi yang baik"
  ];

  // Auth check effect
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    
    try {
      const tokenData = JSON.parse(atob(token.split(".")[1]));
      if (Date.now() >= tokenData.exp * 1000) {
        alert("Sesi Anda telah berakhir. Silakan login kembali.");
        localStorage.removeItem("token");
        navigate("/login");
      }
    } catch (error) {
      console.error("Error decoding token:", error);
      localStorage.removeItem("token");
      navigate("/login");
    }
  }, [navigate]);

  // Fetch child data effect
  useEffect(() => {
    const fetchAnakData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/anak/list", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        
        if (!response.ok) {
          throw new Error("Gagal mengambil data anak");
        }
        
        const data = await response.json();
        setAnakList(Array.isArray(data.data) ? data.data : []);
      } catch (error) {
        console.error("Error fetching child data:", error);
        setErrorMessage(error.message);
        setAnakList([]);
      }
    };
    
    fetchAnakData();
  }, []);

  // Handlers
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleNamaAnakChange = (e) => {
    const selectedNamaAnak = e.target.value;
    const selectedAnak = anakList.find(a => a.nama_anak === selectedNamaAnak);
    
    if (selectedAnak) {
      setFormData(prev => ({
        ...prev,
        id_anak: selectedAnak.id,
        nama_anak: selectedAnak.nama_anak,
        nik: selectedAnak.nik,
        nama_orang_tua: selectedAnak.nama_orang_tua,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setProgress(0);
    setApiResponse(null);
    setErrorMessage("");

    const progressInterval = setInterval(() => {
      setProgress(prev => Math.min(prev + 20, 100));
    }, 500);

    try {
      // Prepare request data
      const requestData = {
        ...formData,
        jenis_kelamin: formData.jenis_kelamin === "Laki-laki" ? 1 : 0,
        umur: parseFloat(formData.umur),
        tinggi_badan: parseFloat(formData.tinggi_badan),
        berat_badan: parseFloat(formData.berat_badan),
      };

      console.log("Submitting data:", requestData);

      // API call
      const response = await fetch("http://127.0.0.1:5000/stunting/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(requestData),
      });

      // Handle response
      const result = await response.json();
      console.log("API response:", result);

      if (!response.ok) {
        throw new Error(result.message || "Prediksi gagal");
      }

      // Process response data
      const responseData = result.data || result;
      
      if (typeof responseData.z_score === 'undefined') {
        throw new Error("Data z_score tidak ditemukan dalam response");
      }

      // Determine status consistently
      const status = responseData.result || 
                    (responseData.z_score < STUNTING_THRESHOLD ? "Stunting" : "Tidak Stunting");

      setApiResponse({
        z_score: parseFloat(responseData.z_score),
        result: status,
        rawData: responseData // Keep original data for debugging
      });

    } catch (error) {
      console.error("Prediction error:", error);
      setErrorMessage(error.message || "Terjadi kesalahan saat memproses prediksi");
    } finally {
      clearInterval(progressInterval);
      setLoading(false);
      setProgress(100);
    }
  };

  // Helper function to determine status
  const getStuntingStatus = (zScore) => {
    return {
      status: zScore < STUNTING_THRESHOLD ? "Stunting" : "Tidak Stunting",
      variant: zScore < STUNTING_THRESHOLD ? "danger" : "success",
      textClass: zScore < STUNTING_THRESHOLD ? "text-danger" : "text-success"
    };
  };

  // Render
  return (
    <div className="d-flex">
      <SideBidan />
      <Container className="mt-4">
        <Navbar bg="light" expand="lg" className="mb-3">
          <Navbar.Brand>Sistem Prediksi Stunting</Navbar.Brand>
        </Navbar>
        
        <Card className="shadow-lg p-4 border-0">
          <h2 className="text-center mb-4 text-primary">Prediksi Stunting</h2>

          {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Nama Anak</Form.Label>
                  <Form.Select
                    name="nama_anak"
                    value={formData.nama_anak}
                    onChange={handleNamaAnakChange}
                    required
                  >
                    <option value="">Pilih Nama Anak</option>
                    {anakList.map(anak => (
                      <option key={anak.id} value={anak.nama_anak}>
                        {anak.nama_anak}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>

              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>NIK</Form.Label>
                  <Form.Control 
                    type="text" 
                    name="nik" 
                    value={formData.nik} 
                    readOnly 
                  />
                </Form.Group>
              </Col>

              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Nama Orang Tua</Form.Label>
                  <Form.Control type="text" name="nama_orang_tua" value={formData.nama_orang_tua} readOnly />
                              </Form.Group>
                            </Col>
                            <Col md={6}>
                              <Form.Group className="mb-3">
                                <Form.Label>Jenis Kelamin</Form.Label>
                                <Form.Select name="jenis_kelamin" value={formData.jenis_kelamin} onChange={handleChange} required>
                                  <option value="">Pilih Jenis Kelamin</option>
                                  <option value="Laki-laki">Laki-laki</option>
                                  <option value="Perempuan">Perempuan</option>
                                </Form.Select>
                              </Form.Group>
                            </Col>
                            <Col md={6}>
                              <Form.Group className="mb-3">
                                <Form.Label>Umur (bulan)</Form.Label>
                                <Form.Control type="number" name="umur" value={formData.umur} onChange={handleChange} required />
                              </Form.Group>
                            </Col>
                            <Col md={6}>
                              <Form.Group className="mb-3">
                                <Form.Label>Tinggi Badan (cm)</Form.Label>
                                <Form.Control type="number" step="0.1" name="tinggi_badan" value={formData.tinggi_badan} onChange={handleChange} required />
                              </Form.Group>
                            </Col>
                            <Col md={6}>
                              <Form.Group className="mb-3">
                                <Form.Label>Berat Badan (kg)</Form.Label>
                                <Form.Control type="number" step="0.1" name="berat_badan" value={formData.berat_badan} onChange={handleChange} required />
                              </Form.Group>
                            </Col>
            </Row>

            {loading && (
              <ProgressBar 
                animated 
                now={progress} 
                label={`${progress}%`} 
                className="mb-3" 
              />
            )}

            <Button 
              variant="primary" 
              type="submit" 
              disabled={loading}
            >
              {loading ? "Memprediksi..." : "Prediksi"}
            </Button>
          </Form>

          {apiResponse && (
            <div className="mt-4">
              <Alert variant={getStuntingStatus(apiResponse.z_score).variant}>
                <h4>Hasil Prediksi</h4>
                <p>
                  <strong>Z-Score:</strong> {apiResponse.z_score.toFixed(2)}
                  <br />
                  <strong>Status:</strong>{" "}
                  <span className={`fw-bold ${getStuntingStatus(apiResponse.z_score).textClass}`}>
                    {apiResponse.result}
                  </span>
                  <br />
                  <small className="text-muted">
                    (Berdasarkan cutoff Z-Score &lt; {STUNTING_THRESHOLD})
                  </small>
                </p>
                
                <hr />
                
                <h5>Detail Input</h5>
                <p><strong>Nama Anak:</strong> {formData.nama_anak}</p>
                <p><strong>Umur:</strong> {formData.umur} bulan</p>
                <p><strong>Tinggi Badan:</strong> {formData.tinggi_badan} cm</p>
                <p><strong>Berat Badan:</strong> {formData.berat_badan} kg</p>
              </Alert>

              {apiResponse.result === "Stunting" && (
                <Card className="mt-3 border-warning">
                  <Card.Header className="bg-warning text-dark">
                    <h5 className="mb-0">Rekomendasi Tindak Lanjut</h5>
                  </Card.Header>
                  <Card.Body>
                    <ol className="mb-0">
                      {stuntingRecommendations.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ol>
                  </Card.Body>
                </Card>
              )}
            </div>
          )}
        </Card>
      </Container>
    </div>
  );
};

export default StuntingPrediction;