<script setup>
import { ref, onMounted } from 'vue'
import BgParticles from '../components/BgParticles.vue'

const categorias = ref([])

onMounted(async () => {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/api/categorias`)
  categorias.value = await res.json()
})
</script>

<template>
  <div class="hero">
    <BgParticles />
    <div class="hero-overlay"></div>
    <div class="scanlines"></div>
    <div class="hero-content">
      <div class="logo-glow"></div>
      <img src="/logo.svg" alt="DnB Awards Spain 2026" class="hero-logo">
      <h1 class="hero-title glitch" data-text="DRUM & BASS">DRUM &amp; BASS</h1>
      <p class="hero-sub-year">AWARDS SPAIN 2026</p>
      <p class="hero-sub">Vota a tus favoritos de la escena DnB nacional</p>
      <div class="hero-actions">
        <router-link to="/categorias" class="btn btn-primary">
          <span>Ver Categorías</span>
          <span class="btn-arrow">→</span>
        </router-link>
        <router-link to="/resultados" class="btn btn-secondary">Resultados en vivo</router-link>
      </div>
    </div>
    <div class="hero-bottom-border"></div>
  </div>

  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Categorías</span>
        <h2>10 formas de brillar</h2>
        <p class="subtitle">DJs, productores, tracks, festivales y más</p>
      </div>
      <div class="grid">
        <div v-for="(cat, i) in categorias" :key="cat.id" class="card">
          <div class="card-glow"></div>
          <span class="card-number">{{ String(i + 1).padStart(2, '0') }}</span>
          <div class="card-icon">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 8v8M8 12h8"/>
            </svg>
          </div>
          <h3>{{ cat.nombre }}</h3>
          <p>{{ cat.descripcion }}</p>
          <router-link :to="`/votar/${cat.id}`" class="btn btn-primary btn-small">
            Votar
            <span class="btn-arrow-small">→</span>
          </router-link>
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="footer-glow"></div>
    <p>DnB Awards Spain 2026 — Kill The Chivato Records</p>
    <p class="small">Vota una vez por categoría. Cada voto cuenta.</p>
  </footer>
</template>
