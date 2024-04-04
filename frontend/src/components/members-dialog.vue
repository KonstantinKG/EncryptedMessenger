<script setup lang="ts">
import ChatService from 'src/api/chat'
import { useRoute } from 'vue-router'
import { computed, ref, watch } from 'vue'
import type { UserData } from 'src/api/users/types'
import { useQuasar } from 'quasar'
import { storeToRefs } from 'pinia'
import { useUserStore } from 'stores/user'

const isOpen = defineModel<boolean>('isOpen', { required: true })

const $q = useQuasar()
const route = useRoute()
const id = computed(() => route.params.id as string)
const members = ref<UserData[]>([])
const ownerId = ref('')

const { user } = storeToRefs(useUserStore())

async function fetchAllMembers() {
  try {
    const { data } = await ChatService.getAllChatMembers(id.value)
    members.value = data
  } catch (e) {
    console.error(e)
  }
}

async function fetchChat() {
  try {
    const { data } = await ChatService.getChat(id.value)
    ownerId.value = data.owner_id
  } catch (e) {
    console.error(e)
  }
}

watch(isOpen, async (e) => {
  if (e) {
    await fetchChat()
    await fetchAllMembers()
  } else {
    members.value = []
  }
})

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

//
// async function addMember() {
//   try {
//     const { data } = await ChatService.addChatMember({
//       chat_id: id.value,
//       members: []
//     })
//   } catch (e) {
//     console.error(e)
//   }
// }
</script>

<template>
  <q-dialog v-model="isOpen">
    <div class="dialog bg-main-dark">
      <q-list separator>
        <q-item v-for="member in members" :key="member.id">
          <q-item-section>
            {{ member.username }}
          </q-item-section>
          <q-item-section v-if="user.id === ownerId" side>
            <q-icon
              style="cursor: pointer"
              color="red"
              size="xs"
              name="delete"
              @click="deleteMember(member)"
            />
          </q-item-section>
          <!--          <q-menu v-if="user.id === ownerId" touch-position context-menu>-->
          <!--            <q-list dense style="min-width: 100px">-->
          <!--              <q-item clickable @click="deleteMember(member)">-->
          <!--                <q-item-section side>-->
          <!--                  <q-icon color="red" size="xs" name="delete" />-->
          <!--                </q-item-section>-->
          <!--                <q-item-section side>удалить {{ member.username }}</q-item-section>-->
          <!--              </q-item>-->
          <!--            </q-list>-->
          <!--          </q-menu>-->
        </q-item>
      </q-list>
    </div>
  </q-dialog>
  <!--    <q-btn color="accent">Добавить участника</q-btn>-->
</template>

<style scoped lang="scss">
.dialog {
  width: 100%;
  max-width: 400px;
  padding: 10px;
}
</style>
