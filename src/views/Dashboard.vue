<template>
  <div>
    <h1>Dashboard</h1>

    <section class="stats">
      <div class="stat-card">
        <div class="stat-value">{{ stats.total }}</div>
        <div class="stat-label">Total Laporan</div>
      </div>
      <div class="stat-card">
        <div class="stat-value selesai">{{ stats.selesai }}</div>
        <div class="stat-label">Selesai</div>
      </div>
      <div class="stat-card">
        <div class="stat-value proses">{{ stats.proses }}</div>
        <div class="stat-label">Dalam Proses</div>
      </div>
      <div class="stat-card">
        <div class="stat-value tertunda">{{ stats.tertunda }}</div>
        <div class="stat-label">Tertunda</div>
      </div>
    </section>

    <ReportForm @saved="loadStats" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import ReportForm from "../components/ReportForm.vue";

const stats = ref({ total: 0, selesai: 0, proses: 0, tertunda: 0 });

async function loadStats() {
  try {
    const response = await api.get("/api/reports");
    const rows = response.data.data;
    stats.value = {
      total: rows.length,
      selesai: rows.filter((r) => r.status === "Selesai").length,
      proses: rows.filter((r) => r.status === "Dalam Proses").length,
      tertunda: rows.filter((r) => r.status === "Tertunda").length,
    };
  } catch (error) {
    console.error("Gagal memuat statistik:", error);
  }
}

onMounted(loadStats);
</script>

<style scoped>
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1e3a8a;
}

.stat-value.selesai {
  color: #15803d;
}

.stat-value.proses {
  color: #854d0e;
}

.stat-value.tertunda {
  color: #b91c1c;
}

.stat-label {
  margin-top: 6px;
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
}
</style>
