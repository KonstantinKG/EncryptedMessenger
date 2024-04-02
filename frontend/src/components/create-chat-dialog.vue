<script setup lang="ts">
import { computed, ref } from 'vue'
import ChatService from 'src/api/chat'
import UsersService from 'src/api/users'
import SearchService from 'src/api/search'
import { AllUsersData, UserData } from 'src/api/users/types'
import { FILES_PATH } from 'src/constants'
import PersonIcon from 'src/icons/person.vue'

const emit = defineEmits<{ (e: 'onCreated'): void }>()
const isOpen = defineModel<boolean>('isOpen', { required: true })

const name = ref('')
const image = ref<File>()
const previewImage = ref('')
const members = ref<UserData[]>([])
const page = ref(1)
const usersData = ref<AllUsersData>({
  current: 1,
  pages: 0,
  total: 0,
  data: []
})
const step = ref(1)
const scrollTarget = ref()

function onSelectAvatar(target: HTMLInputElement) {
  const file = target.files?.[0]
  target.value = ''

  if (file) {
    image.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

function addMember(user: UserData) {
  const index = members.value.findIndex((member) => member.id == user.id)
  if (index !== -1) {
    members.value.splice(index, 1)
  } else {
    members.value.push(user)
  }
}

async function createChat() {
  try {
    const formData = new FormData()
    formData.append('name', name.value)
    if (image.value) {
      formData.append('image', image.value)
    }
    if (members.value.length) {
      formData.append(
        'members',
        members.value.map((el) => el.id)
      )
    }
    await ChatService.createChat(formData)
    emit('onCreated')
    isOpen.value = false
  } catch (e) {
    console.error(e)
  }
}

async function fetchUsers() {
  try {
    const { data } = await UsersService.getAllUsers(page.value)
    if (data.current > 1) {
      usersData.value.current = data.current
      usersData.value.data = usersData.value.data.concat(data.data)
    } else {
      usersData.value = data
    }
  } catch (e) {
    console.error(e)
  }
}

async function loadMoreUsers(index: number, done: (stop?: boolean) => void) {
  page.value++
  await fetchUsers()
  done(usersData.value.current > usersData.value.pages)
}

const searchUsersName = ref('')
const searchUsersPage = ref(1)

async function searchUsers() {
  try {
    const { data } = await SearchService.searchUsers({
      username: searchUsersName.value,
      page: searchUsersPage.value
    })
    if (data.current > 1) {
      usersData.value.current = data.current
      usersData.value.data = usersData.value.data.concat(data.data)
    } else {
      usersData.value = data
    }
  } catch (e) {
    console.error(e)
  }
}

fetchUsers()

const isValid = computed(() => name.value)

function nextStep() {
  if (!isValid.value) return
  step.value++
}
</script>

<template>
  <q-dialog v-model="isOpen">
    <div class="dialog bg-dark">
      <div v-if="step === 1" class="content">
        <label class="cursor-pointer">
          <q-avatar color="primary" text-color="white" size="70px">
            <q-img v-if="previewImage || image" :src="previewImage || image" alt="image" />
            <q-icon v-else name="photo_camera" />
          </q-avatar>
          <input
            accept=".jpg, .jpeg, .png, .svg, .webp, .avif"
            type="file"
            hidden
            @change="onSelectAvatar($event.target as HTMLInputElement)"
          />
        </label>
        <q-input v-model="name" filled label="Название чата" />
        <!--        error-message="Обязательное поле"-->
        <!--        :error="!isValid"-->
      </div>
      <div v-else class="users scroll" style="max-height: 400px">
        <div class="users__title">
          Всего пользователей: <span class="text-grey">{{ usersData.total }}</span>
        </div>
        <q-input
          v-model="searchUsersName"
          filled
          label="Искать пользователей"
          @keyup.enter="searchUsers"
        />
        <div v-if="members.length" class="users__chips">
          <q-chip
            v-for="(member, index) in members"
            :key="member.id"
            color="primary"
            removable
            :label="member.username"
            @remove="members.splice(index, 1)"
          />
        </div>
        <q-list ref="scrollTarget">
          <q-infinite-scroll @load="loadMoreUsers">
            <q-item
              v-for="user in usersData.data"
              :key="user.id"
              v-ripple
              clickable
              @click="addMember(user)"
            >
              <q-item-section>
                <q-avatar font-size="40px">
                  <q-img v-if="user.image" :src="`${FILES_PATH}${user.image}`" alt="User avatar" />
                  <person-icon v-else />
                </q-avatar>
              </q-item-section>
              <q-item-section avatar>
                {{ user.username }}
              </q-item-section>
            </q-item>
            <template #loading>
              <div class="row justify-center q-my-md">
                <q-spinner name="dots" size="40px" />
              </div>
            </template>
          </q-infinite-scroll>
        </q-list>
      </div>
      <div class="actions">
        <template v-if="step === 1">
          <q-btn v-close-popup flat>Отмена</q-btn>
          <q-btn flat @click="nextStep">Далее</q-btn>
        </template>
        <template v-else>
          <q-btn flat @click="step--">Назад</q-btn>
          <q-btn flat @click="createChat">Создать</q-btn>
        </template>
      </div>
    </div>
  </q-dialog>
</template>

<style scoped lang="scss">
.dialog {
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.content {
  display: flex;
  align-items: center;
  gap: 20px;

  .q-input {
    flex: 1 1 auto;
  }
}

.users {
  display: flex;
  flex-direction: column;
  gap: 10px;

  &__title {
    font-size: 18px;
  }

  &__chips {
    display: flex;
    flex-wrap: wrap;
  }
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
}
</style>
