<template>
  <section class="table-card">
    <div class="header">
      <h2>Daftar Laporan</h2>
      <button class="refresh" @click="$emit('refresh')">Muat Ulang</button>
    </div>

    <div v-if="loading" class="state">Memuat data...</div>

    <div v-else-if="reports.length === 0" class="state">
      Belum ada laporan. Silakan tambahkan laporan pertama Anda.
    </div>

    <table v-else>
      <thead>
        <tr>
          <th>No</th>
          <th>Judul Tugas</th>
          <th>Deskripsi</th>
          <th>Tanggal</th>
          <th>Status</th>
          <th>Lampiran</th>
          <th>Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(report, index) in reports" :key="report._id">
          <td>{{ index + 1 }}</td>
          <td class="judul">{{ report.judul_tugas }}</td>
          <td class="deskripsi">{{ report.deskripsi }}</td>
          <td>{{ formatDate(report.tanggal) }}</td>
          <td>
            <span class="badge" :class="statusClass(report.status)">
              {{ report.status }}
            </span>
          </td>
          <td>
            <a
              v-if="report.attachment_url"
              :href="report.attachment_url"
              target="_blank"
              rel="noopener noreferrer"
              class="attachment"
            >
              Buka
            </a>
            <span v-else class="muted">-</span>
          </td>
          <td class="actions-col">
            <button class="btn-edit" @click="$emit('edit', report)">Edit</button>
            <button class="btn-delete" @click="$emit('delete', report)">Hapus</button>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
defineProps({
  reports: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["refresh", "edit", "delete"]);

function formatDate(date) {
  if (!date) return "-";
  const parts = date.split("-");
  if (parts.length !== 3) return date;
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Agu",
    "Sep",
    "Okt",
    "Nov",
    "Des",
  ];
  return `${parts[2]} ${months[Number(parts[1]) - 1]} ${parts[0]}`;
}

function statusClass(status) {
  switch (status) {
    case "Selesai":
      return "selesai";
    case "Dalam Proses":
      return "proses";
    case "Tertunda":
      return "tertunda";
    default:
      return "";
  }
}
</script>

<style scoped>
.table-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  overflow-x: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

h2 {
  margin: 0;
  color: #1e3a8a;
}

.refresh {
  background: #e5e7eb;
  color: #1f2937;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.refresh:hover {
  background: #d1d5db;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th,
td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: top;
}

th {
  background: #f9fafb;
  color: #374151;
  font-weight: 600;
  white-space: nowrap;
}

.judul {
  font-weight: 600;
  min-width: 150px;
}

.deskripsi {
  color: #4b5563;
  white-space: pre-wrap;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.selesai {
  background: #dcfce7;
  color: #15803d;
}

.proses {
  background: #fef9c3;
  color: #854d0e;
}

.tertunda {
  background: #fee2e2;
  color: #b91c1c;
}

.attachment {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.attachment:hover {
  text-decoration: underline;
}

.muted {
  color: #9ca3af;
}

.actions-col {
  white-space: nowrap;
}

.btn-edit,
.btn-delete {
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  margin-right: 6px;
}

.btn-edit {
  background: #dbeafe;
  color: #1d4ed8;
}

.btn-edit:hover {
  background: #bfdbfe;
}

.btn-delete {
  background: #fee2e2;
  color: #b91c1c;
}

.btn-delete:hover {
  background: #fecaca;
}

.state {
  color: #6b7280;
  text-align: center;
  padding: 24px;
}
</style>
