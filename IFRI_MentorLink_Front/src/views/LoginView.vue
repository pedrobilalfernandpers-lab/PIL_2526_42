<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const identifier = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

const showResetModal = ref(false)
const resetData = ref({
  identifier: '',
  new_password: ''
})

const handleLogin = async () => {
  errorMsg.value = ''
  loading.value = true
  
  try {
    const res = await axios.post('/api/auth/login', {
      identifier: identifier.value,
      password: password.value
    })
    
    localStorage.setItem('token', res.data.access_token)
    router.push('/dashboard')
    
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      errorMsg.value = err.response.data.detail
    } else {
      errorMsg.value = "Erreur de connexion au serveur."
    }
  } finally {
    loading.value = false
  }
}

const handleResetPassword = async () => {
  try {
    const res = await axios.post('/api/auth/reset-password', resetData.value)
    alert(res.data.message)
    showResetModal.value = false
    resetData.value = { identifier: '', new_password: '' }
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors de la réinitialisation.")
  }
}
</script>

<template>
  <div class="flex justify-center items-center py-16 px-4">
    <div class="w-full max-w-md bg-white rounded-3xl shadow-xl shadow-gray-200/50 p-8 border border-gray-100">
      <div class="text-center mb-10">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Bon retour 👋</h2>
        <p class="text-gray-500">Connectez-vous pour retrouver vos mentors.</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div v-if="errorMsg" class="bg-red-50 text-red-600 p-3 rounded-xl text-sm text-center">
          {{ errorMsg }}
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email ou Téléphone</label>
          <input 
            v-model="identifier" 
            type="text" 
            required
            class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors"
            placeholder="etudiant@ifri.bj"
          >
        </div>
        
        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="block text-sm font-medium text-gray-700">Mot de passe</label>
            <button type="button" @click="showResetModal = true" class="text-sm text-brand font-medium hover:underline">Oublié ?</button>
          </div>
          <input 
            v-model="password" 
            type="password" 
            required
            class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors"
            placeholder="••••••••"
          >
        </div>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-brand hover:bg-brand-dark text-white py-3.5 rounded-xl font-medium shadow-md shadow-blue-500/20 transition-all disabled:opacity-70 flex justify-center items-center"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>
      
      <div class="mt-8 text-center text-sm text-gray-500">
        Nouveau sur MentorLink ? 
        <router-link to="/register" class="text-brand font-medium hover:underline">Créer un compte</router-link>
      </div>
    </div>

    <!-- Modal Reset Password -->
    <div v-if="showResetModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50 p-4">
      <div class="bg-white p-8 rounded-3xl w-full max-w-sm shadow-2xl">
        <h2 class="text-2xl font-bold mb-2">Mot de passe oublié</h2>
        <p class="text-gray-500 text-sm mb-6">Réinitialisez votre mot de passe avec votre email ou téléphone.</p>
        <form @submit.prevent="handleResetPassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Identifiant</label>
            <input v-model="resetData.identifier" type="text" required class="w-full px-4 py-3 bg-gray-50 rounded-xl border-transparent focus:border-brand focus:ring-0" placeholder="Email ou Téléphone">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nouveau mot de passe</label>
            <input v-model="resetData.new_password" type="password" required class="w-full px-4 py-3 bg-gray-50 rounded-xl border-transparent focus:border-brand focus:ring-0" placeholder="••••••••">
          </div>
          <div class="flex gap-3 pt-4">
            <button type="button" @click="showResetModal = false" class="flex-1 bg-gray-100 text-gray-700 py-3 rounded-xl font-medium hover:bg-gray-200 transition">Annuler</button>
            <button type="submit" class="flex-1 bg-brand text-white py-3 rounded-xl font-medium hover:bg-brand-dark transition shadow-sm">Valider</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>