from app import create_app  # Import fungsi create_app dari __init__.py

app = create_app()  # Panggil fungsi untuk membuat aplikasi Flask

if __name__ == '__main__':
    app.run(debug=True)  # Jalankan server Flask
