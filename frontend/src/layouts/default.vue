<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import CreateChatDialog from 'components/create-chat-dialog.vue'
import ChatService from 'src/api/chat'
import SearchService from 'src/api/search'
import { useChatStore } from 'stores/chat'
import { storeToRefs } from 'pinia'
import { FILES_PATH } from 'src/constants'
import { AllChatsData } from 'src/api/chat/types'
import PersonIcon from 'src/icons/person.vue'
import LogoIcon from 'src/icons/logo.vue'


const { sendMessage } = useChatStore()
const { message, file } = storeToRefs(useChatStore())

const chats = ref<AllChatsData>({
  total: 0,
  pages: 0,
  current: 1,
  data: []
})
const page = ref(1)
const isCreateChatDialogOpen = ref(false)

async function fetchChats() {
  try {
    const { data } = await ChatService.getAllChats(page.value)
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

fetchChats()

const searchChatsName = ref('')
const searchChatsPage = ref(1)

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

function onSelectFile(target: HTMLInputElement) {
  const selectedFile = target.files?.[0]
  target.value = ''
  if (selectedFile) {
    file.value = selectedFile
  }
}

const pageWrapper = ref<HTMLElement | null>(null)
async function onSend() {
  await sendMessage(currentChat.value.id)
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="WAL__layout shadow-3">
    <q-header elevated>
      <q-toolbar class="bg-main-secondary">
        <q-btn round flat>
          <q-avatar>
            <q-img
              v-if="currentChat?.image"
              :src="`${FILES_PATH}${currentChat.image}`"
              alt="Chat avatar"
            />
            <person-icon v-else />
          </q-avatar>
        </q-btn>

        <span class="q-subtitle-1 q-pl-md">
          {{ currentChat?.name }}
        </span>

        <q-space />

        <q-btn round flat icon="search" />
        <q-btn round flat>
          <q-icon name="attachment" class="rotate-135" />
        </q-btn>
        <q-btn round flat icon="more_vert">
          <q-menu auto-close :offset="[110, 0]">
            <q-list style="min-width: 150px">
              <q-item clickable>
                <q-item-section>Contact data</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Block</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Select messages</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Silence</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Clear messages</q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>Erase messages</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>
    <q-drawer :model-value="true" show-if-above bordered :breakpoint="690">
      <q-toolbar class="bg-main-secondary">
        <q-avatar font-size="40px">
          <logo-icon />
        </q-avatar>
        <q-space />
        <q-btn round flat icon="more_vert">
          <q-menu auto-close :offset="[110, 8]">
            <q-list style="min-width: 150px">
              <q-item clickable>
                <q-item-section>Профиль</q-item-section>
              </q-item>
              <q-item clickable @click="isCreateChatDialogOpen = true">
                <q-item-section>Новый чат</q-item-section>
              </q-item>
              <q-item clickable to="/login">
                <q-item-section>Выйти</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
      <q-toolbar class="bg-main-secondary">
        <q-input
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
            <q-item-section avatar>
              <q-avatar font-size="40px">
                <q-img v-if="chat.image" :src="`${FILES_PATH}${chat.image}`" alt="Chat avatar" />
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

    <q-page-container ref="pageWrapper" class="bg-main-secondary">
      <router-view />
    </q-page-container>

    <q-footer>
      <q-toolbar class="chat-toolbar">
        <q-input
          v-model="message"
          class="full-width"
          standout="bg-main text-white"
          label="Введите сообщение"
          clearable
          color="red"
          @keyup.enter="onSend"
        />
        <label class="cursor-pointer">
          <q-icon size="25px" name="attachment" class="rotate-135" />
          <input type="file" hidden @change="onSelectFile($event.target as HTMLInputElement)" />
        </label>
      </q-toolbar>
    </q-footer>
  </q-layout>

  <create-chat-dialog v-model:is-open="isCreateChatDialogOpen" @on-created="fetchChats" />
</template>

<style scoped lang="scss">
.chat-toolbar {
  padding-left: 0;
  gap: 10px;
  color: #fff;
}
</style>
