# Hospital API

## Deskripsi
API ini dibuat untuk membantu proses pendataan pegawai, dokter, pasien, dan appointment di klinik atau rumah sakit. Aplikasi ini mencakup fitur login, manajemen data pegawai, dokter, pasien, serta pembuatan appointment antara pasien dan dokter. Dan ditujukan untuk menyelesaikan test yang diberikan.

## Fitur Utama
- Authentication dengan JWT
- Manajemen Pegawai (CRUD)
- Manajemen Dokter (CRUD)
- Manajemen Pasien (CRUD)
- Scheduler untuk sinkronisasi data pasien dengan Google BigQuery (In Progress)
- Swagger untuk dokumentasi API

## Instalasi

1. Clone repository ini:

2. Masuk ke dalam direktori project:

    ```bash
    cd hospital_api
    ```

3. Buat virtual environment dan aktifkan:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Atur environment variables di file `.env`:

    ```env
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/db_name
    ```

6. Migrasi database:

    ```bash
    docker-compose build
    docker-compose exec web flask db init
    docker-compose exec web flask db migrate -m "Initial migration"
    docker-compose exec web flask db upgrade
    ```

7. Jalankan aplikasi:

    ```bash
    docker-compose up --build
    ```

8. Untuk melihat dokumentasi API, buka di `http://localhost:5000/swagger`.

## Struktur Project

```plaintext
hospital_api/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── employees.py
│   │   ├── doctors.py
│   │   ├── patients.py
│   │   └── appointments.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── employee_service.py
│   │   ├── doctor_service.py
│   │   ├── patient_service.py
│   │   └── appointment_service.py
│   ├── requests/
│   │   ├── employee_request.py
│   │   ├── doctor_request.py
│   │   ├── patient_request.py
│   │   └── appointment_request.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── bigquery.py
│   │   └── scheduler.py
│   └── swagger/
│       ├── __init__.py
│       └── swagger_config.py
│
├── migrations/
│
├── tests/
│   ├── __init__.py
│   └── test_endpoints.py
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
