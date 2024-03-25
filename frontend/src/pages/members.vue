<script setup lang="ts">
import ChatService from 'src/api/chat'
import { useRoute } from 'vue-router'
import { computed, ref } from 'vue'
import type { UserData } from 'src/api/users/types'

const route = useRoute()
const id = computed(() => route.params.id as string)

const members = ref<UserData[]>([])

async function fetchAllMembers() {
  try {
    const { data } = await ChatService.getAllChatMembers(id.value)
    members.value = data
  } catch (e) {
    console.error(e)
  }
}

fetchAllMembers()
</script>

<template>
  <q-page>
    <div v-for="member in members" :key="member.id">{{ member.username }}</div>
  </q-page>
</template>

<style scoped lang="scss"></style>
