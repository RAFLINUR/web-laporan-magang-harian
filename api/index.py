import os
from datetime import datetime

import cloudinary
import cloudinary.uploader
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
CORS(app)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.get_database()
reports_collection = db["reports"]


@app.route("/api/reports", methods=["POST"])
def create_report():
    judul_tugas = request.form.get("judul_tugas")
    deskripsi = request.form.get("deskripsi")
    tanggal = request.form.get("tanggal")
    status = request.form.get("status")

    if not judul_tugas or not deskripsi or not tanggal or not status:
        return jsonify({"error": "judul_tugas, deskripsi, tanggal, dan status wajib diisi"}), 400

    file = request.files.get("dokumen")

    attachment_url = None
    public_id = None
    if file and file.filename:
        try:
            uploaded = cloudinary.uploader.upload(
                file,
                folder="laporan-magang",
                resource_type="raw",
                public_id=f"laporan-magang/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}",
            )
            attachment_url = uploaded["secure_url"]
            public_id = uploaded["public_id"]
        except Exception as exc:
            return jsonify({"error": f"Gagal mengunggah file ke Cloudinary: {str(exc)}"}), 500

    report = {
        "judul_tugas": judul_tugas,
        "deskripsi": deskripsi,
        "tanggal": tanggal,
        "status": status,
        "attachment_url": attachment_url,
        "attachment_public_id": public_id,
        "dibuat_pada": datetime.now().isoformat(),
    }

    result = reports_collection.insert_one(report)
    report["_id"] = str(result.inserted_id)

    return jsonify({"message": "Laporan berhasil disimpan", "data": report}), 201


@app.route("/api/reports", methods=["GET"])
def get_reports():
    reports = list(reports_collection.find().sort("tanggal", 1))
    for report in reports:
        report["_id"] = str(report["_id"])
    return jsonify({"data": reports}), 200


@app.route("/api/reports/<report_id>", methods=["GET"])
def get_report(report_id):
    try:
        obj_id = ObjectId(report_id)
    except Exception:
        return jsonify({"error": "ID laporan tidak valid"}), 400

    report = reports_collection.find_one({"_id": obj_id})
    if not report:
        return jsonify({"error": "Laporan tidak ditemukan"}), 404

    report["_id"] = str(report["_id"])
    return jsonify({"data": report}), 200


@app.route("/api/reports/<report_id>", methods=["PUT"])
def update_report(report_id):
    judul_tugas = request.form.get("judul_tugas")
    deskripsi = request.form.get("deskripsi")
    tanggal = request.form.get("tanggal")
    status = request.form.get("status")

    if not judul_tugas or not deskripsi or not tanggal or not status:
        return jsonify({"error": "judul_tugas, deskripsi, tanggal, dan status wajib diisi"}), 400

    try:
        obj_id = ObjectId(report_id)
    except Exception:
        return jsonify({"error": "ID laporan tidak valid"}), 400

    existing = reports_collection.find_one({"_id": obj_id})
    if not existing:
        return jsonify({"error": "Laporan tidak ditemukan"}), 404

    update = {
        "judul_tugas": judul_tugas,
        "deskripsi": deskripsi,
        "tanggal": tanggal,
        "status": status,
        "diperbarui_pada": datetime.now().isoformat(),
    }

    file = request.files.get("dokumen")
    if file and file.filename:
        try:
            uploaded = cloudinary.uploader.upload(
                file,
                folder="laporan-magang",
                resource_type="raw",
                public_id=f"laporan-magang/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}",
            )
            old_public_id = existing.get("attachment_public_id")
            if old_public_id:
                try:
                    cloudinary.uploader.destroy(old_public_id, resource_type="raw")
                except Exception:
                    pass
            update["attachment_url"] = uploaded["secure_url"]
            update["attachment_public_id"] = uploaded["public_id"]
        except Exception as exc:
            return jsonify({"error": f"Gagal mengunggah file ke Cloudinary: {str(exc)}"}), 500

    reports_collection.update_one({"_id": obj_id}, {"$set": update})

    updated = reports_collection.find_one({"_id": obj_id})
    updated["_id"] = str(updated["_id"])

    return jsonify({"message": "Laporan berhasil diperbarui", "data": updated}), 200


@app.route("/api/reports/<report_id>", methods=["DELETE"])
def delete_report(report_id):
    try:
        obj_id = ObjectId(report_id)
    except Exception:
        return jsonify({"error": "ID laporan tidak valid"}), 400

    existing = reports_collection.find_one({"_id": obj_id})
    if not existing:
        return jsonify({"error": "Laporan tidak ditemukan"}), 404

    old_public_id = existing.get("attachment_public_id")
    if old_public_id:
        try:
            cloudinary.uploader.destroy(old_public_id, resource_type="raw")
        except Exception:
            pass

    reports_collection.delete_one({"_id": obj_id})

    return jsonify({"message": "Laporan berhasil dihapus"}), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Laporan Harian Magang berjalan!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
