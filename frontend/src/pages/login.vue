<script setup lang="ts">
import { reactive } from 'vue'

const form = reactive({
  username: '',
  password: '',
  image: ''
})
</script>

<template>
  <q-form>
    <q-input v-model="form.username" />
    <q-input type="password" v-model="form.password" />
    <q-input type="file" v-model="form.image" />
  </q-form>
</template>

<style scoped>

</style>
