<script setup lang="ts">
import CreateChatDialog from 'components/create-chat-dialog.vue'
import AttachmentDialog from 'components/attachment-dialog.vue'
import PersonalDialog from 'components/personal-dialog.vue'
import PersonIcon from 'src/icons/person.vue'
import LogoIcon from 'src/icons/logo.vue'
import { ref, computed, watch } from 'vue'
import SearchService from 'src/api/search'
import { useChatStore } from 'stores/chat'
import { useUserStore } from 'stores/user'
import { useQuasar } from 'quasar'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { FILES_PATH } from 'src/constants'
import { AllChatsData } from 'src/api/chat/types'
import type { UserData } from 'src/api/users/types'
import ChatService from 'src/api/chat'

const $q = useQuasar()
const router = useRouter()

const idAccess = $q.localStorage.getItem('id_access') as string
if (idAccess) {
  useUserStore().fetchUser(idAccess)
}

const { user } = storeToRefs(useUserStore())

const { sendMessage, searchMessages, deleteChat, fetchChats } = useChatStore()
const { message, file, searchMessagesName, chats } = storeToRefs(useChatStore())
const isCreateChatDialogOpen = ref(false)
const isPersonalDialogOpen = ref(false)
const searchChatsName = ref('')
const searchChatsPage = ref(1)
const drawer = ref(true)
const drawerMini = ref(false)
const isMembers = ref(false)

async function searchChats() {
  try {
    const { data } = await SearchService.searchChats({
      name: searchChatsName.value,
      page: searchChatsPage.value
    })
    if (data.current > 1) {
      chats.value.current = data.current
      chats.value.data = chats.value.data.concat(data.data)
    } else {
      chats.value = data
    }
  } catch (e) {
    console.error(e)
  }
}

const currentChatIndex = ref(0)

const currentChat = computed(() => {
  return chats.value.data[currentChatIndex.value]
})

function setCurrentChat(index: number) {
  currentChatIndex.value = index
}

watch(searchChatsName, async () => {
  await searchChats()
})

watch(searchMessagesName, async () => {
  await searchMessages(currentChat.value.id)
})

const isAttachmentDialogOpen = ref(false)

function onSelectFile(target: HTMLInputElement) {
  const selectedFile = target.files?.[0]
  target.value = ''
  if (selectedFile) {
    file.value = selectedFile
    isAttachmentDialogOpen.value = true
  }
}

function onExit() {
  $q.localStorage.remove('id_access')
  router.push('/login')
}

async function onSend() {
  await sendMessage(currentChat.value.id)
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}

fetchChats()

const members = ref<UserData[]>([])

async function fetchAllMembers(id: string) {
  try {
    const { data } = await ChatService.getAllChatMembers(id)
    members.value = data
  } catch (e) {
    console.error(e)
  }
}

const currentMembersLength = computed(() => {
  if (members.value.length) {
    const lastDigit = members.value.length % 10
    const lastTwoDigits = members.value.length % 100
    if (lastTwoDigits >= 11 && lastTwoDigits <= 19) {
      return `${members.value.length} участников`
    } else if (lastDigit === 1) {
      return `${members.value.length} участник`
    } else if (lastDigit >= 2 && lastDigit <= 4) {
      return `${members.value.length} участника`
    } else {
      return `${members.value.length} участников`
    }
  } else {
    return ''
  }
})

watch(currentChat, (value) => {
  if (value) fetchAllMembers(value.id)
})
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar class="bg-main-secondary" style="gap: 10px">
        <q-btn v-if="isMembers" flat icon="chevron_left" to="" @click="isMembers = false" />
        <q-avatar font-size="40px">
          <img
            v-if="currentChat?.image"
            :src="`${FILES_PATH}${currentChat.image}`"
            alt="Chat avatar"
          />
          <person-icon v-else />
        </q-avatar>
        <div>
          <div>{{ currentChat?.name }}</div>
          <div>{{ currentMembersLength }}</div>
        </div>
        <q-input
          v-model="searchMessagesName"
          style="flex: 1 1 auto"
          rounded
          outlined
          dense
          placeholder="Искать по сообщениям"
          :debounce="300"
          clearable
          @clear="searchMessagesName = ''"
          @keyup.enter="searchMessages(currentChat.id)"
        >
          <template #prepend>
            <q-icon name="search" />
          </template>
        </q-input>
        <!--        <q-btn round flat icon="more_vert">-->
        <!--          <q-menu auto-close touch-position>-->
        <!--            <q-list style="min-width: 150px">-->
        <!--              <q-item-->
        <!--                clickable-->
        <!--                :to="{-->
        <!--                  name: 'Members',-->
        <!--                  params: { id: currentChat.id }-->
        <!--                }"-->
        <!--                @click="isMembers = true"-->
        <!--              >-->
        <!--                <q-item-section>Участники</q-item-section>-->
        <!--              </q-item>-->
        <!--            </q-list>-->
        <!--          </q-menu>-->
        <!--        </q-btn>-->
      </q-toolbar>
    </q-header>
    <q-drawer v-model="drawer" :mini="drawerMini" bordered :breakpoint="690">
      <q-toolbar class="bg-main-secondary">
        <q-avatar font-size="40px" class="cursor-pointer" @click="drawerMini = !drawerMini">
          <logo-icon />
        </q-avatar>
        <q-space />
        <q-btn round flat icon="more_vert">
          <q-menu auto-close :offset="[110, 8]">
            <q-list style="min-width: 150px">
              <q-item clickable @click="isPersonalDialogOpen = true">
                <q-item-section>Профиль</q-item-section>
              </q-item>
              <q-item clickable @click="isCreateChatDialogOpen = true">
                <q-item-section>Новый чат</q-item-section>
              </q-item>
              <q-item clickable @click="onExit">
                <q-item-section>Выйти</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
      <q-toolbar class="bg-main-secondary">
        <q-input
          v-if="!drawerMini"
          v-model="searchChatsName"
          rounded
          outlined
          dense
          class="full-width"
          placeholder="Искать"
          :debounce="300"
          @keyup.enter="searchChats"
        >
          <template #prepend>
            <q-icon name="search" />
          </template>
        </q-input>
        <q-btn
          v-else
          dense
          size="14px"
          outline
          round
          icon="search"
          @click="drawerMini = !drawerMini"
        />
      </q-toolbar>
      <q-scroll-area style="height: calc(100% - 100px)" class="bg-main">
        <q-list>
          <q-item
            v-for="(chat, index) in chats.data"
            :key="chat.id"
            clickable
            active-class="text-white bg-main-dark"
            :to="{
              name: 'Chat',
              params: { id: chat.id }
            }"
            @click="setCurrentChat(index)"
          >
            <q-menu touch-position context->
              <q-list dense style="min-width: 100px">
                <q-item clickable @click="deleteChat(chat)">
                  <q-item-section side>удалить чат</q-item-section>
                  <q-item-section thumbnail>
                    <q-icon color="red" size="xs" name="delete" />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
            <q-item-section avatar>
              <q-avatar font-size="40px">
                <img v-if="chat.image" :src="`${FILES_PATH}${chat.image}`" alt="Chat avatar" />
                <person-icon v-else />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              {{ chat.name }}
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container class="bg-main-secondary">
      <router-view />
    </q-page-container>

    <q-footer>
      <q-toolbar class="chat-toolbar bg-secondary">
        <q-input
          v-model="message"
          class="full-width"
          label="Введите сообщение"
          clearable
          borderless
          bg-color="secondary"
          @keyup.enter="onSend"
        />
        <label class="cursor-pointer">
          <q-icon size="25px" name="attachment" class="rotate-135" />
          <input type="file" hidden @change="onSelectFile($event.target as HTMLInputElement)" />
        </label>
      </q-toolbar>
    </q-footer>
  </q-layout>
  <personal-dialog v-model:is-open="isPersonalDialogOpen" />
  <attachment-dialog v-model:is-open="isAttachmentDialogOpen" :file="file" />
  <create-chat-dialog v-model:is-open="isCreateChatDialogOpen" @on-created="fetchChats" />
</template>

<style scoped lang="scss">
.chat-toolbar {
  gap: 10px;
}
</style>
