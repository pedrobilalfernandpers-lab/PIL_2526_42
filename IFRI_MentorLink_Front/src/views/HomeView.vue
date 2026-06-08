<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[80vh] px-4 text-center">
    <div class="inline-flex items-center justify-center p-3 bg-brand-light rounded-2xl mb-8">
      <svg class="w-12 h-12 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    </div>
    
    <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight mb-6">
      L'entraide académique,<br/>
      <span class="text-brand">réinventée.</span>
    </h1>
    
    <p class="text-xl text-gray-500 max-w-2xl mb-10 leading-relaxed">
      Trouvez le mentor idéal parmi les étudiants de l'IFRI. Progressez plus vite, comprenez mieux, et réussissez ensemble.
    </p>
    
    <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
      <button @click="router.push('/register')" class="bg-brand hover:bg-brand-dark text-white px-8 py-4 rounded-full text-lg font-medium shadow-lg shadow-blue-500/30 transition-all hover:-translate-y-0.5">
        Commencer maintenant
      </button>
      <button @click="router.push('/login')" class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 px-8 py-4 rounded-full text-lg font-medium transition-all shadow-sm">
        J'ai déjà un compte
      </button>
    </div>
  </div>
</template>