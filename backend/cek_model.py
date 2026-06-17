import pickle

model_path = "models/logistic_regression_model.pkl"

try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    print("✅ Model berhasil di-load!")
    print(model)  # Cek isi model
except Exception as e:
    print("❌ Gagal load model:", str(e))
