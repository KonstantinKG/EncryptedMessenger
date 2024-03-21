<template>
  <router-view />
</template>

<script setup lang="ts">
import { useUserStore } from 'stores/user'
import { useQuasar } from 'quasar'

const $q = useQuasar()

useUserStore().fetchUser($q.cookies.get('id_access'))
</script>
