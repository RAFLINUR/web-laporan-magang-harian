<template>
  <header class="navbar">
    
    <!-- Bungkus logo dan judul di dalam satu div ini -->
    <div class="brand-container">
      <img src="/stechoq-logo.png" alt="Logo Stechoq" class="logo" />
      <div class="brand">Web Laporan Harian Magang Rafli.</div>
    </div>

    <!-- Navigasi tetap di luar bungkus tadi -->
    <nav class="nav-right">
      <router-link to="/" class="nav-link" exact-active-class="active">
        Dashboard
      </router-link>
      <router-link to="/laporan" class="nav-link" active-class="active">
        Daftar Laporan
      </router-link>
    </nav>
    
  </header>
  <main>
    <router-view />
  </main>
</template>

<style>
:root {
  color-scheme: light;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

body {
  margin: 0;
  background: #f4f6f9;
  color: #1f2937;
}

.navbar {
  background: #568496;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 24px;
  box-shadow: 0 2px 4px rgba(14, 70, 255, 0.192);
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  font-weight: 700;
  font-size: 17px;
}

nav {
  display: flex;
  gap: 8px;
}

.brand-container {
  display: flex;
  align-items: center;
  gap: 15px; /* Memberikan jarak agar logo dan teks tidak menempel */
}

.nav-link {
  color: #dbeafe;
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
}

.nav-link:hover {
  background: #27429a;
  color: #ffffff;
}

.nav-link.active {
  background: #2563eb;
  color: #ffffff;
}

.logo {
  height: 40px;         /* Patokan tinggi logo */
  max-width: 200px;     /* Batas maksimal lebar agar tidak menabrak menu */
  object-fit: contain;  /* Memastikan logo mengecil secara proporsional tanpa gepeng */
}

main {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px;
}

h1 {
  text-align: center;
  margin-bottom: 24px;
  color: #1e3a8a;
}

@media (max-width: 600px) {
  .navbar {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
