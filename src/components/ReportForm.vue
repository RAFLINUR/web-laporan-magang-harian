<template>
  <section class="form-card">
    <h2>{{ isEditing ? "Edit Laporan Harian" : "Input Laporan Harian" }}</h2>

    <form @submit.prevent="submitReport">
      <div class="field">
        <label for="judul">Judul Tugas</label>
        <input
          id="judul"
          v-model="form.judul_tugas"
          type="text"
          placeholder="Masukkan judul tugas"
          required
        />
      </div>

      <div class="field">
        <label for="deskripsi">Deskripsi</label>
        <textarea
          id="deskripsi"
          v-model="form.deskripsi"
          rows="4"
          placeholder="Jelaskan kegiatan yang dilakukan"
          required
        ></textarea>
      </div>

      <div class="field-row">
        <div class="field">
          <label for="tanggal">Tanggal</label>
          <input id="tanggal" v-model="form.tanggal" type="date" required />
        </div>

        <div class="field">
          <label for="status">Status</label>
          <select id="status" v-model="form.status" required>
            <option value="Selesai">Selesai</option>
            <option value="Dalam Proses">Dalam Proses</option>
            <option value="Tertunda">Tertunda</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label for="dokumen">Lampiran Dokumen (Opsional)</label>
        <input
          id="dokumen"
          type="file"
          @change="handleFileChange"
          accept=".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg"
        />
        <small v-if="isEditing && !selectedFile.value" class="hint">
          Kosongkan jika tidak ingin mengganti lampiran saat ini.
        </small>
      </div>

      <p v-if="selectedFileName" class="file-name">
        File terpilih: {{ selectedFileName }}
      </p>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>

      <div class="actions">
        <button type="submit" :disabled="loading">
          {{ loading ? "Mengirim..." : isEditing ? "Perbarui Laporan" : "Simpan Laporan" }}
        </button>
        <button v-if="isEditing" type="button" class="cancel" @click="$emit('cancel-edit')">
          Batal
        </button>
      </div>
    </form>
  </section>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import api from "../services/api";

const props = defineProps({
  editing: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["saved", "cancel-edit"]);

const isEditing = ref(false);

const form = reactive({
  judul_tugas: "",
  deskripsi: "",
  tanggal: "",
  status: "Selesai",
});

const selectedFile = ref(null);
const selectedFileName = ref("");
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

function resetForm() {
  form.judul_tugas = "";
  form.deskripsi = "";
  form.tanggal = "";
  form.status = "Selesai";
  selectedFile.value = null;
  selectedFileName.value = "";
  const input = document.getElementById("dokumen");
  if (input) input.value = "";
}

watch(
  () => props.editing,
  (report) => {
    if (report) {
      isEditing.value = true;
      form.judul_tugas = report.judul_tugas;
      form.deskripsi = report.deskripsi;
      form.tanggal = report.tanggal;
      form.status = report.status;
      selectedFile.value = null;
      selectedFileName.value = "";
      const input = document.getElementById("dokumen");
      if (input) input.value = "";
    } else {
      isEditing.value = false;
      resetForm();
    }
  }
);

function handleFileChange(event) {
  const file = event.target.files[0];
  selectedFile.value = file || null;
  selectedFileName.value = file ? file.name : "";
}

async function submitReport() {
  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  const formData = new FormData();
  formData.append("judul_tugas", form.judul_tugas);
  formData.append("deskripsi", form.deskripsi);
  formData.append("tanggal", form.tanggal);
  formData.append("status", form.status);

  if (selectedFile.value) {
    formData.append("dokumen", selectedFile.value);
  }

  try {
    let response;
    if (isEditing.value) {
      response = await api.put(`/api/reports/${props.editing._id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } else {
      response = await api.post("/api/reports", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    }
    successMessage.value = response.data.message;

    resetForm();
    emit("saved");
  } catch (error) {
    errorMessage.value =
      error.response?.data?.error || "Terjadi kesalahan saat menyimpan laporan.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.form-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

h2 {
  margin-top: 0;
  color: #1e3a8a;
}

.field {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.field-row {
  display: flex;
  gap: 16px;
}

.field-row .field {
  flex: 1;
}

label {
  font-weight: 600;
  margin-bottom: 6px;
}

input,
textarea,
select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #2563eb;
}

button {
  background: #2563eb;
  color: #ffffff;
  border: none;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  background: #1d4ed8;
}

button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.cancel {
  background: #e5e7eb;
  color: #1f2937;
}

.cancel:hover {
  background: #d1d5db;
}

.file-name {
  font-size: 13px;
  color: #374151;
}

.hint {
  font-size: 12px;
  color: #6b7280;
  margin-top: 6px;
}

.error {
  color: #b91c1c;
  background: #fee2e2;
  padding: 8px 12px;
  border-radius: 6px;
}

.success {
  color: #15803d;
  background: #dcfce7;
  padding: 8px 12px;
  border-radius: 6px;
}

@media (max-width: 600px) {
  .field-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>
