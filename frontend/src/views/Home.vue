<script setup>
import { ref, onMounted } from 'vue'
const categorias = ref([])

onMounted(async () => {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/categorias`)
  categorias.value = await res.json()
})
</script>

<template>
  <div class="hero">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <img src="/logo.svg" alt="DnB Awards Spain 2026" class="hero-logo">
      <h1 class="hero-title">DRUM &amp; BASS<br>AWARDS SPAIN</h1>
      <p class="hero-year">2026</p>
      <p class="hero-sub">Vota a tus favoritos de la escena DnB nacional</p>
      <div class="hero-actions">
        <router-link to="/categorias" class="btn btn-primary">Ver Categorías</router-link>
        <router-link to="/resultados" class="btn btn-secondary">Resultados</router-link>
      </div>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <h2>10 Categorías</h2>
      <p class="subtitle">DJs, productores, tracks, festivales y más</p>
      <div class="grid">
        <div v-for="(cat, i) in categorias" :key="cat.id" class="card">
          <span class="card-number">{{ String(i + 1).padStart(2, '0') }}</span>
          <h3>{{ cat.nombre }}</h3>
          <p>{{ cat.descripcion }}</p>
          <router-link :to="`/votar/${cat.id}`" class="btn btn-primary btn-small">Votar</router-link>
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <p>DnB Awards Spain 2026 — Kill The Chivato Records</p>
    <p class="small">Vota una vez por categoría. Cada voto cuenta.</p>
  </footer>
</template>
