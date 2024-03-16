<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-toggle :model-value="isDarkMode" @update:model-value="toggleTheme" />
      <router-view />
      <q-page-sticky position="bottom-right" :offset="[18, 18]">
        <q-btn fab icon="add" color="accent" />
      </q-page-sticky>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

defineOptions({
  name: 'MainLayout'
})

const $q = useQuasar()
const isDarkMode = ref($q.dark.isActive)

function toggleTheme(value: boolean) {
  isDarkMode.value = value
  $q.dark.set(value)
}
</script>
