<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { initWebSocket, disconnectWebSocket, wsNotifications, unreadGlobalCount } from './services/wsService'

const router = useRouter()
const route = useRoute()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

// Connexion/Déconnexion automatique du WebSocket
watch(isAuthenticated, (newVal) => {
  if (newVal) {
    initWebSocket()
  } else {
    disconnectWebSocket()
  }
}, { immediate: true })

const logout = () => {
  localStorage.removeItem('token')
  disconnectWebSocket()
  router.push('/login')
}

// Gestion des Toasts (notifications visuelles flottantes)
const toasts = ref([])
let toastCounter = 0

watch(wsNotifications, (newVal, oldVal) => {
  // On prend la dernière notification reçue
  if (newVal.length > 0) {
    const latestMsg = newVal[newVal.length - 1]
    
    // Si l'utilisateur est déjà sur la page de chat ET sur la bonne conversation, 
    // on ne montre pas la petite popup (pas besoin de le spammer s'il lit déjà).
    const isCurrentlyChatting = route.path === '/chat'
    // Pour simplifier, on montre le toast s'il n'est pas sur le chat du tout
    if (!isCurrentlyChatting) {
      const toastId = toastCounter++
      toasts.value.push({
        id: toastId,
        sender_name: latestMsg.sender_name,
        content: latestMsg.content
      })
      
      // Auto-disparition après 5 secondes
      setTimeout(() => {
        toasts.value = toasts.value.filter(t => t.id !== toastId)
      }, 5000)
    }
  }
}, { deep: true })

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

const goToChat = (id) => {
  removeToast(id)
  router.push('/chat')
}
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <!-- Navbar minimaliste Blanc/Bleu -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center cursor-pointer" @click="router.push('/')">
            <span class="text-2xl font-bold text-brand">MentorLink</span>
            <span class="ml-2 text-sm font-medium text-gray-500 hidden sm:block">IFRI</span>
          </div>
          
          <div class="flex items-center space-x-6">
            <template v-if="!isAuthenticated">
              <router-link to="/login" class="text-gray-600 hover:text-brand font-medium transition-colors">Connexion</router-link>
              <router-link to="/register" class="bg-brand hover:bg-brand-dark text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">S'inscrire</router-link>
            </template>
            <template v-else>
              <router-link to="/chat" class="text-gray-600 hover:text-brand font-medium transition-colors relative flex items-center">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                Messages
                <span v-if="unreadGlobalCount > 0" class="absolute -top-2 -right-3 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full animate-bounce">
                  {{ unreadGlobalCount }}
                </span>
              </router-link>
              <router-link to="/dashboard" class="text-gray-600 hover:text-brand font-medium transition-colors">Tableau de bord</router-link>
              <button @click="logout" class="text-red-500 hover:text-red-700 font-medium transition-colors">Déconnexion</button>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow">
      <router-view />
    </main>

    <!-- Footer minimaliste -->
    <footer class="bg-white border-t border-gray-100 py-8 mt-12">
      <div class="max-w-6xl mx-auto px-4 text-center text-gray-400 text-sm">
        &copy; 2026 IFRI MentorLink. Projet Intégrateur.
      </div>
    </footer>

    <!-- Conteneur des Toasts -->
    <div class="fixed bottom-6 right-6 z-[100] flex flex-col gap-3 pointer-events-none">
      <div v-for="toast in toasts" :key="toast.id" 
           class="bg-white border-l-4 border-brand shadow-2xl rounded-r-xl p-4 flex gap-4 min-w-[300px] max-w-sm items-start transform transition-all duration-300 translate-y-0 opacity-100 pointer-events-auto">
        
        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-brand-light text-brand flex items-center justify-center font-bold">
          {{ toast.sender_name.charAt(0) }}
        </div>
        
        <div class="flex-grow">
          <div class="text-xs text-gray-500 font-medium uppercase tracking-wider mb-0.5">Nouveau message</div>
          <div class="text-sm font-bold text-gray-900 truncate">{{ toast.sender_name }}</div>
          <div class="text-sm text-gray-600 mt-1 line-clamp-2 leading-snug">{{ toast.content }}</div>
          
          <div class="mt-3 flex gap-3">
            <button @click="goToChat(toast.id)" class="text-xs bg-brand text-white px-3 py-1.5 rounded-lg font-medium hover:bg-brand-dark transition-colors">Répondre</button>
            <button @click="removeToast(toast.id)" class="text-xs text-gray-400 hover:text-gray-600 font-medium">Fermer</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>