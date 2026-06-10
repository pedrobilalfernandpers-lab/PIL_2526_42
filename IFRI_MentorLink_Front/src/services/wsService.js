import { ref } from 'vue'

export const wsNotifications = ref([])
export const unreadGlobalCount = ref(0)
export const activeWebSocket = ref(null)

export const initWebSocket = () => {
  const token = localStorage.getItem('token')
  if (!token) return

  if (activeWebSocket.value) return // Déjà connecté

  const wsUrl = `ws://127.0.0.1:8000/api/ws?token=${token}`
  const ws = new WebSocket(wsUrl)
  activeWebSocket.value = ws

  ws.onopen = () => console.log("WebSocket global connecté.")

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      if (data.type === 'new_message') {
        // Ajouter la notif dans la file globale
        const notif = {
          id: Date.now(),
          ...data.message,
          conversation_id: data.conversation_id
        }
        wsNotifications.value.push(notif)
        unreadGlobalCount.value++
      }
    } catch (e) {
      console.error("Erreur WS parsing:", e)
    }
  }

  ws.onclose = () => {
    console.log("WebSocket global déconnecté.")
    activeWebSocket.value = null
  }
}

export const disconnectWebSocket = () => {
  if (activeWebSocket.value) {
    activeWebSocket.value.close()
    activeWebSocket.value = null
  }
}