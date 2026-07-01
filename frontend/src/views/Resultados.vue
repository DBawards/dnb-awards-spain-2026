<script setup>
import { ref, onMounted } from 'vue'
const resultados = ref([])
const categorias = ref({})

onMounted(async () => {
  const [resRes, catRes] = await Promise.all([
    fetch(`${import.meta.env.VITE_API_URL}/api/resultados`),
    fetch(`${import.meta.env.VITE_API_URL}/api/categorias`)
  ])
  const cats = await catRes.json()
  cats.forEach(c => { categorias.value[c.id] = c.nombre })
  const rows = await resRes.json()
  const grouped = {}
  rows.forEach(r => {
    if (!grouped[r.categoria]) grouped[r.categoria] = []
    grouped[r.categoria].push(r)
  })
  resultados.value = grouped
})
</script>

<template>
  <div class="page">
    <div class="container">
      <h1>Resultados</h1>
      <p class="subtitle">Clasificación actual de las votaciones</p>

      <div v-for="(nominados, cat) in resultados" :key="cat" class="result-group">
        <h2>{{ cat }}</h2>
        <div class="result-bar-container">
          <div v-for="(n, i) in nominados" :key="n.id" class="result-row">
            <span class="result-pos">{{ i + 1 }}</span>
            <div class="result-info">
              <span class="result-artist">{{ n.artista }}</span>
              <span v-if="n.track" class="result-track">{{ n.track }}</span>
            </div>
            <div class="result-bar-wrapper">
              <div class="result-bar" :style="{ width: Math.max((n.votos / nominados[0].votos) * 100, 5) + '%' }"></div>
            </div>
            <span class="result-votes">{{ n.votos }} votos</span>
          </div>
        </div>
      </div>

      <div v-if="Object.keys(resultados).length === 0" class="empty">
        <p>Todavía no hay votos. ¡Sé el primero!</p>
        <router-link to="/categorias" class="btn btn-primary">Votar ahora</router-link>
      </div>
    </div>
  </div>
</template>
