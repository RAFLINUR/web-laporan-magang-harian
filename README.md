# Web Laporan Harian Magang (Logbook)

Aplikasi logbook harian magang dengan arsitektur Monorepo, siap deploy ke Vercel.

## Teknologi

- **Frontend:** Vue 3 + Vite
- **Backend:** Flask (Python) sebagai Serverless Function di Vercel
- **Database:** MongoDB (PyMongo)
- **Storage:** Cloudinary (lampiran file)

## Struktur Folder

```
├── api/
│   ├── index.py          # Flask API (routes)
│   └── requirements.txt  # Dependensi Python
├── src/
│   ├── components/
│   │   ├── ReportForm.vue    # Form input + edit
│   │   └── ReportTable.vue   # Daftar laporan
│   ├── services/
│   │   └── api.js            # Axios instance
│   ├── App.vue
│   └── main.js
├── vercel.json
├── package.json
├── vite.config.js
└── index.html
```

## API Endpoints

| Method | Endpoint                     | Deskripsi                          |
|--------|------------------------------|------------------------------------|
| POST   | `/api/reports`               | Membuat laporan (multipart/form-data) |
| GET    | `/api/reports`               | Mengambil semua laporan            |
| PUT    | `/api/reports/:id`           | Memperbarui laporan                |
| DELETE | `/api/reports/:id`           | Menghapus laporan + lampiran       |

Field teks: `judul_tugas`, `deskripsi`, `tanggal`, `status`.
Field file (opsional): `dokumen`.

## Setup Lokal

### 1. Backend
```bash
# Buat virtualenv (opsional tapi disarankan)
python3 -m venv venv
source venv/bin/activate

# Install dependensi
pip install -r api/requirements.txt

# Jalankan server (default port 5000)
python api/index.py
```

### 2. Frontend
```bash
npm install
npm run dev
```

Vite proxy `/api` ke `localhost:5000`, jadi akses app di `http://localhost:5173`.

## Variabel Environment

Buat file `.env` / set di Vercel:

```
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/<database>
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Deploy ke Vercel

1. Push repo ke GitHub.
2. Import ke Vercel dengan **Framework Preset: Vite**.
3. Tambahkan env vars di atas (Settings → Environment Variables).
4. Deploy. `vercel.json` otomatis mengarahkan `/api/*` ke Flask dan sisanya ke build Vue.

> Catatan: nama file `.env` diabaikan untuk hanya berisi contoh — untuk produksi selalu set env vars di Vercel dashboard.
