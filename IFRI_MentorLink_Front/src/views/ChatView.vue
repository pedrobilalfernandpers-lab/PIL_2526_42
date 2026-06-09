<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const conversations = ref([])
const messages = ref([])
const activeConvId = ref(null)
const newMessage = ref('')
const loading = ref(true)

const getToken = () => localStorage.getItem('token')

const fetchConversations = async () => {
  try {
    const res = await axios.get('/api/conversations', { headers: { Authorization: `Bearer ${getToken()}` } })
    conversations.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const selectConversation = async (id) => {
  activeConvId.value = id
  try {
    const res = await axios.get(`/api/conversations/${id}/messages`, { headers: { Authorization: `Bearer ${getToken()}` } })
    messages.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !activeConvId.value) return
  try {
    await axios.post(`/api/conversations/${activeConvId.value}/messages`, { content: newMessage.value }, { headers: { Authorization: `Bearer ${getToken()}` } })
    newMessage.value = ''
    selectConversation(activeConvId.value) // refresh
    fetchConversations() // refresh sidebar
  } catch (err) {
    console.error(err)
  }
}

const rejectMatch = async (matchId) => {
  if (!confirm("Voulez-vous vraiment rompre ce match et supprimer cette conversation ?")) return
  try {
    await axios.put(`/api/matches/${matchId}/reject`, {}, { headers: { Authorization: `Bearer ${getToken()}` } })
    activeConvId.value = null
    fetchConversations()
  } catch (err) {
    alert("Erreur lors de la rupture.")
  }
}

onMounted(fetchConversations)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8 h-[85vh] flex gap-6">
    <!-- Sidebar -->
    <div class="w-1/3 bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">
      <div class="p-6 border-b border-gray-100">
        <h2 class="text-xl font-bold text-gray-900">Discussions</h2>
      </div>
      <div class="overflow-y-auto flex-grow p-2">
        <div v-if="loading" class="text-center p-4 text-gray-400">Chargement...</div>
        <div v-for="c in conversations" :key="c.id" 
             @click="selectConversation(c.id)"
             class="p-4 rounded-2xl cursor-pointer transition-colors mb-1"
             :class="activeConvId === c.id ? 'bg-brand-light' : 'hover:bg-gray-50'">
          <div class="flex justify-between items-start">
            <div class="font-bold text-gray-900">{{ c.other_user_name }}</div>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider"
                  :class="c.role === 'Mentor' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'">
              {{ c.role }}
            </span>
          </div>
          <div class="text-xs font-medium text-gray-500 mt-1">📚 {{ c.subject }}</div>
          <div class="text-sm text-gray-500 truncate mt-1">{{ c.last_message || 'Nouvelle conversation' }}</div>
        </div>
        <div v-if="!loading && conversations.length === 0" class="text-center p-6 text-gray-400 text-sm">
          Aucune conversation. Acceptez un match pour discuter !
        </div>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="w-2/3 bg-white rounded-3xl border border-gray-100 shadow-sm flex flex-col overflow-hidden">
      <template v-if="activeConvId">
        <!-- Chat Header -->
        <div class="p-6 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
          <h2 class="font-bold text-gray-900">
            Conversation avec {{ conversations.find(c => c.id === activeConvId)?.other_user_name }}
          </h2>
          <button @click="rejectMatch(conversations.find(c => c.id === activeConvId)?.match_id)" class="text-sm text-red-500 hover:text-red-700 hover:underline">
            Rompre le match
          </button>
        </div>
        <!-- Messages -->
        <div class="flex-grow overflow-y-auto p-6 space-y-4">
          <div v-for="m in messages" :key="m.id" class="flex flex-col" :class="m.sender_name.includes(' ') ? '' : ''">
            <div class="text-xs text-gray-400 mb-1 px-1">{{ m.sender_name }}</div>
            <div class="px-4 py-2.5 rounded-2xl max-w-[80%] w-fit bg-brand-light text-gray-800">
              {{ m.content }}
            </div>
          </div>
        </div>
        <!-- Input -->
        <div class="p-4 border-t border-gray-100 bg-white">
          <form @submit.prevent="sendMessage" class="flex gap-2">
            <input v-model="newMessage" type="text" placeholder="Écrivez un message..." class="flex-grow px-4 py-3 rounded-full bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0">
            <button type="submit" class="bg-brand text-white px-6 rounded-full font-medium hover:bg-brand-dark transition-colors">
              Envoyer
            </button>
          </form>
        </div>
      </template>
      <div v-else class="flex-grow flex items-center justify-center text-gray-400 flex-col">
        <svg class="w-16 h-16 mb-4 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
        <p>Sélectionnez une discussion à gauche</p>
      </div>
    </div>
  </div>
</template>