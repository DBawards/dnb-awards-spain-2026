<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({ id: String })
const categoria = ref(null)
const nominados = ref([])
const selected = ref(null)
const voted = ref(false)
const voterHash = ref('')
const error = ref('')

onMounted(() => {
  voterHash.value = 'anon-' + Math.random().toString(36).slice(2, 10)
  load()
})

async function load() {
  const [catRes, nomRes] = await Promise.all([
    fetch('http://localhost:8000/api/categorias'),
    fetch(`http://localhost:8000/api/nominaciones/${props.id}`)
  ])
  const cats = await catRes.json()
  categoria.value = cats.find(c => c.id === Number(props.id))
  nominados.value = await nomRes.json()
}

async function votar() {
  if (!selected.value) return
  error.value = ''
  try {
    const res = await fetch('http://localhost:8000/api/votar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nominacion_id: selected.value, voter_hash: voterHash.value })
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || 'Error al votar')
    }
    voted.value = true
    load()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="page">
    <div class="container">
      <router-link to="/categorias" class="back-link">← Categorías</router-link>
      <h1 v-if="categoria">{{ categoria.nombre }}</h1>
      <p class="subtitle" v-if="categoria">{{ categoria.descripcion }}</p>

      <div v-if="voted" class="alert alert-success">
        ¡Voto emitido correctamente!
      </div>
      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <div class="nominees">
        <div v-for="n in nominados" :key="n.id"
          :class="['nominee-card', { selected: selected === n.id }]"
          @click="selected = n.id; voted = false">
          <div class="nominee-info">
            <h3>{{ n.artista }}</h3>
            <p v-if="n.track" class="track">{{ n.track }}</p>
            <p v-if="n.descripcion" class="desc">{{ n.descripcion }}</p>
          </div>
          <div class="nominee-votes">
            <span class="vote-count">{{ n.votos }}</span>
            <span class="vote-label">votos</span>
          </div>
          <div :class="['radio', { active: selected === n.id }]">
            <div class="radio-dot"></div>
          </div>
        </div>
      </div>

      <button v-if="selected && !voted" class="btn btn-primary btn-large" @click="votar">
        Votar
      </button>
    </div>
  </div>
</template>
