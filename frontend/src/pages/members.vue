<script setup lang="ts">
import ChatService from 'src/api/chat'
import { useRoute } from 'vue-router'
import { computed, ref } from 'vue'
import type { UserData } from 'src/api/users/types'
import { useQuasar } from 'quasar'

const $q = useQuasar()
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

async function deleteMember(member: UserData) {
  try {
    const { data } = await ChatService.deleteChatMember({
      chat_id: id.value,
      members: [member.id]
    })
    const index = members.value.findIndex((el) => el.id === member.id)
    members.value.splice(index, 1)
    $q.notify({
      message: 'Пользователь успешно удален!',
      color: 'primary',
      position: 'top-right',
      timeout: 3000,
      actions: [
        {
          icon: 'close',
          color: 'white',
          round: true,
          handler: () => {}
        }
      ]
    })
  } catch (e) {
    $q.notify({
      message: e.response.data.errors[0],
      color: 'red',
      position: 'top-right',
      timeout: 3000,
      actions: [
        {
          icon: 'close',
          color: 'white',
          round: true,
          handler: () => {}
        }
      ]
    })
    console.error(e)
  }
}

async function addMember() {
  try {
    const { data } = await ChatService.addChatMember({
      chat_id: id.value,
      members: []
    })
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <q-page>
    <q-btn color="accent">Добавить участника</q-btn>
    <q-list dense>
      <q-item v-for="member in members" :key="member.id">
        {{ member.username }}
        <q-menu touch-position context-menu>
          <q-list dense style="min-width: 100px">
            <q-item clickable @click="deleteMember(member)">
              <q-item-section side>
                <q-icon color="red" size="xs" name="delete" />
              </q-item-section>
              <q-item-section side>удалить участника</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-item>
    </q-list>
  </q-page>
</template>

<style scoped lang="scss"></style>
