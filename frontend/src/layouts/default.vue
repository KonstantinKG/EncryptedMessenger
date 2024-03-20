<template>
  <div class="WAL position-relative bg-main-dark" :style="style">
    <q-layout view="lHh Lpr lFf" class="WAL__layout shadow-3" container>
      <q-header elevated>
        <q-toolbar class="bg-main-secondary text-black">
          <q-btn
            round
            flat
            icon="keyboard_arrow_left"
            class="WAL__drawer-open q-mr-sm"
            @click="toggleLeftDrawer"
          />

          <q-btn round flat>
            <q-avatar>
              <img :src="currentConversation.avatar" />
            </q-avatar>
          </q-btn>

          <span class="q-subtitle-1 q-pl-md">
            {{ currentConversation.person }}
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

      <q-drawer v-model="leftDrawerOpen" show-if-above bordered :breakpoint="690">
        <q-toolbar class="bg-main-secondary">
          <q-avatar class="cursor-pointer">
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo.svg" />
          </q-avatar>

          <q-space />

          <q-btn round flat icon="message" />
          <q-btn round flat icon="more_vert">
            <q-menu auto-close :offset="[110, 8]">
              <q-list style="min-width: 150px">
                <q-item clickable>
                  <q-item-section>Профиль</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Новый чат</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Выйти</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn round flat icon="close" class="WAL__drawer-close" @click="toggleLeftDrawer" />
        </q-toolbar>

        <q-toolbar class="bg-main-secondary">
          <q-input
            v-model="search"
            rounded
            outlined
            dense
            class="WAL__field full-width"
            bg-color="dark"
            placeholder="Search or start a new conversation"
          >
            <template #prepend>
              <q-icon name="search" />
            </template>
          </q-input>
        </q-toolbar>

        <q-scroll-area style="height: calc(100% - 100px)" class="bg-main">
          <q-list>
            <q-item
              v-for="(conversation, index) in conversations"
              :key="conversation.id"
              v-ripple
              clickable
              @click="setCurrentConversation(index)"
            >
              <q-item-section avatar>
                <q-avatar>
                  <img :src="conversation.avatar" />
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label lines="1">
                  {{ conversation.person }}
                </q-item-label>
                <q-item-label class="conversation__summary" caption>
                  <q-icon v-if="conversation.sent" name="check" />
                  <q-icon v-if="conversation.deleted" name="not_interested" />
                  {{ conversation.caption }}
                </q-item-label>
              </q-item-section>

              <q-item-section side>
                <q-item-label caption>
                  {{ conversation.time }}
                </q-item-label>
                <q-icon name="keyboard_arrow_down" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container class="bg-main-secondary">
        <router-view />
      </q-page-container>

      <!--      <q-footer>-->
      <!--        <q-toolbar class="bg-main-secondary text-black row">-->
      <!--          <q-input-->
      <!--            v-model="message"-->
      <!--            rounded-->
      <!--            outlined-->
      <!--            dense-->
      <!--            class="WAL__field col-grow q-mr-sm"-->
      <!--            bg-color="main"-->
      <!--            placeholder="Введите сообщение"-->
      <!--          />-->
      <!--        </q-toolbar>-->
      <!--      </q-footer>-->
    </q-layout>
  </div>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { ref, computed } from 'vue'
import EncryptedMessengerService from 'src/api'

const conversations = [
  {
    id: 1,
    person: 'Razvan Stoenescu',
    avatar: 'https://cdn.quasar.dev/team/razvan_stoenescu.jpeg',
    caption: "I'm working on Quasar!",
    time: '15:00',
    sent: true
  },
  {
    id: 2,
    person: 'Dan Popescu',
    avatar: 'https://cdn.quasar.dev/team/dan_popescu.jpg',
    caption: "I'm working on Quasar!",
    time: '16:00',
    sent: true
  },
  {
    id: 3,
    person: 'Jeff Galbraith',
    avatar: 'https://cdn.quasar.dev/team/jeff_galbraith.jpg',
    caption: "I'm working on Quasar!",
    time: '18:00',
    sent: true
  },
  {
    id: 4,
    person: 'Allan Gaunt',
    avatar: 'https://cdn.quasar.dev/team/allan_gaunt.png',
    caption: "I'm working on Quasar!",
    time: '17:00',
    sent: true
  }
]

const $q = useQuasar()

const chats = ref({
  total: 0,
  pages: 0,
  current: 1,
  data: []
})
const page = ref(1)

const socket = new WebSocket('ws://localhost:8201')

socket.onopen = (e) => {
  socket.send(
    JSON.stringify({
      type: 'listen',
      user_id: $q.cookies.get('id_access')
    })
  )
}

socket.onmessage = (event) => {
  console.log(event.data)
}

socket.onclose = () => {
  console.log('closed')
}

socket.onerror = (e) => {
  console.error(e)
}

async function getChats() {
  try {
    const { data } = await EncryptedMessengerService.getAllChats(page.value)
    chats.value = data
  } catch (e) {
    console.error(e)
  }
}

getChats()

const leftDrawerOpen = ref(false)
const search = ref('')
const message = ref('')
const currentConversationIndex = ref(0)

const currentConversation = computed(() => {
  return conversations[currentConversationIndex.value]
})

const style = computed(() => ({
  height: $q.screen.height + 'px'
}))

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function setCurrentConversation(index) {
  currentConversationIndex.value = index
}
</script>

<style lang="sass">
.WAL
  width: 100%
  height: 100%
  padding-top: 20px
  padding-bottom: 20px

  &:before
    content: ''
    height: 127px
    position: fixed
    top: 0
    width: 100%
    background-color: $main-dark

  &__layout
    margin: 0 auto
    z-index: 4000
    height: 100%
    width: 90%
    max-width: 950px
    border-radius: 5px

  &__field.q-field--outlined .q-field__control:before
    border: none

  .q-drawer--standard
    .WAL__drawer-close
      display: none

@media (max-width: 850px)
  .WAL
    padding: 0

    &__layout
      width: 100%
      border-radius: 0

@media (min-width: 691px)
  .WAL
    &__drawer-open
      display: none

.conversation__summary
  margin-top: 4px

.conversation__more
  margin-top: 0 !important
  font-size: 1.4rem
</style>
