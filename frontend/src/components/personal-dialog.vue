<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useUserStore } from 'stores/user'
import { storeToRefs } from 'pinia'
import { FILES_PATH } from 'src/constants'
import UsersService from 'src/api/users'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const isOpen = defineModel<boolean>('isOpen', { required: true })
const { selfUpdate } = useUserStore()
const { user } = storeToRefs(useUserStore())

const router = useRouter()
const $q = useQuasar()
const isEdit = ref(false)
const previewImage = ref('')
let initialUser: null = null

watch(user, (e) => {
  initialUser = JSON.parse(JSON.stringify(user.value))
})

function onSelectAvatar(target: HTMLInputElement) {
  const file = target.files?.[0]
  target.value = ''

  if (file) {
    user.value.image = file
    previewImage.value = URL.createObjectURL(file)
  }
}

async function onDelete() {
  await UsersService.selfDelete()
  $q.localStorage.remove('id_access')
  await router.push('/login')
}

function onCancel() {
  user.value = JSON.parse(JSON.stringify(initialUser))
  previewImage.value = ''
  isEdit.value = false
}

function onDeletePhoto() {
  user.value.image = null
  previewImage.value = ''
}
</script>

<template>
  <q-dialog v-model="isOpen">
    <div class="dialog bg-main-dark">
      <div class="content">
        <div class="photo">
          <q-avatar color="primary" text-color="white" size="100px">
            <img
              v-if="previewImage || user.image"
              :src="previewImage || `${FILES_PATH}${user.image}`"
              alt="image"
            />
            <q-icon v-else name="cloud_upload" />
          </q-avatar>
          <label v-if="isEdit" class="cursor-pointer">
            Поменять фото
            <input
              accept=".jpg, .jpeg, .png, .svg, .webp, .avif"
              type="file"
              hidden
              @change="onSelectAvatar($event.target as HTMLInputElement)"
            />
          </label>
          <!--          <q-btn-->
          <!--            v-if="isEdit"-->
          <!--            no-caps-->
          <!--            size="13px"-->
          <!--            color="red"-->
          <!--            outline-->
          <!--            rounded-->
          <!--            @click="onDeletePhoto"-->
          <!--          >-->
          <!--            Удалить фото-->
          <!--          </q-btn>-->
        </div>
        <q-input v-model="user.username" :readonly="!isEdit" />
      </div>
      <!--      <q-btn no-caps color="red" to="/register" @click="onDelete">Удалить аккаунт </q-btn>-->
      <div class="actions">
        <q-btn v-if="!isEdit" flat icon="edit" dense @click="isEdit = true" />
        <template v-else>
          <q-btn no-caps flat color="red" dense @click="onCancel">Отмена</q-btn>
          <q-btn v-close-popup no-caps flat dense @click="selfUpdate"> Сохранить</q-btn>
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
  padding: 20px;
}

.content {
  display: flex;
  align-items: center;
  gap: 20px;

  .photo {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;

    label {
      border: 1px solid $primary;
      padding: 5px 10px;
      border-radius: 30px;
    }
  }

  .q-input {
    flex: 1 1 auto;
  }
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
}
</style>
