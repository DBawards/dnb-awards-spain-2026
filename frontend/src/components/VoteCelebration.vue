<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let anim = null

const emit = defineEmits(['done'])

onMounted(() => {
  const c = canvas.value
  const ctx = c.getContext('2d')
  c.width = window.innerWidth
  c.height = window.innerHeight

  const colors = ['#ff0055', '#ff4400', '#00ff88', '#00ccff', '#ffffff']
  const particles = []
  for (let i = 0; i < 80; i++) {
    particles.push({
      x: c.width / 2 + (Math.random() - 0.5) * 100,
      y: c.height / 2,
      vx: (Math.random() - 0.5) * 12,
      vy: -Math.random() * 14 - 4,
      size: Math.random() * 6 + 3,
      color: colors[Math.floor(Math.random() * colors.length)],
      life: 1,
      gravity: 0.2 + Math.random() * 0.1,
    })
  }

  let frame = 0
  function burst() {
    ctx.clearRect(0, 0, c.width, c.height)
    frame++
    let alive = false

    particles.forEach(p => {
      p.x += p.vx
      p.vy += p.gravity
      p.y += p.vy
      p.vx *= 0.99
      p.life -= 0.008

      if (p.life > 0) {
        alive = true
        ctx.globalAlpha = p.life
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2)
        ctx.fillStyle = p.color
        ctx.fill()
      }
    })

    ctx.globalAlpha = 1
    if (alive && frame < 300) {
      anim = requestAnimationFrame(burst)
    } else {
      emit('done')
    }
  }
  burst()

  onUnmounted(() => cancelAnimationFrame(anim))
})
</script>

<template>
  <canvas ref="canvas" class="celebration" />
</template>

<style scoped>
.celebration {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  pointer-events: none;
}
</style>
