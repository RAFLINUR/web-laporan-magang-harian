<template>
  <div>
    <h1>Daftar Laporan</h1>

    <ReportForm
      v-if="editing"
      :editing="editing"
      @saved="onSaved"
      @cancel-edit="cancelEdit"
    />

    <ReportTable
      :reports="reports"
      :loading="loading"
      @refresh="loadReports"
      @edit="onEdit"
      @delete="onDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import ReportForm from "../components/ReportForm.vue";
import ReportTable from "../components/ReportTable.vue";

const reports = ref([]);
const loading = ref(false);
const editing = ref(null);

async function loadReports() {
  loading.value = true;
  try {
    const response = await api.get("/api/reports");
    reports.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil daftar laporan:", error);
  } finally {
    loading.value = false;
  }
}

function onEdit(report) {
  editing.value = { ...report };
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function onSaved() {
  editing.value = null;
  loadReports();
}

function cancelEdit() {
  editing.value = null;
}

async function onDelete(report) {
  if (!confirm(`Hapus laporan "${report.judul_tugas}"?`)) return;
  try {
    await api.delete(`/api/reports/${report._id}`);
    loadReports();
  } catch (error) {
    console.error("Gagal menghapus laporan:", error);
  }
}

onMounted(loadReports);
</script>