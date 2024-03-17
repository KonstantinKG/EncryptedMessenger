<script setup lang="ts">
import { reactive, ref } from 'vue'
import EncryptedMessengerService from 'src/api'
import { Register } from 'src/api/types'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const router = useRouter()
const $q = useQuasar()
const form = reactive<Register>({
  username: '',
  password: '',
  image: undefined
})
const previewAvatar = ref('')
const isPassword = ref(true)

function onSelectAvatar(target: HTMLInputElement) {
  const file = target.files?.[0]
  target.value = ''

  if (file) {
    form.image = file
    previewAvatar.value = URL.createObjectURL(file)
  }
}

async function onSubmit() {
  try {
    const formData = new FormData()
    for (const key in form) {
      formData.append(key, form[key])
    }
    const { data } = await EncryptedMessengerService.register(formData)
    $q.cookies.set('id_access', data.id)
    $q.notify({
      message: 'Аккаунт успешно заегестрирован!',
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
    await router.push('/chats')
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
</script>

<template>
  <div class="container">
    <q-form class="form" @submit.prevent="onSubmit">
      <q-input v-model="form.username" label="Введите никнейм" />
      <q-input
        v-model="form.password"
        :type="isPassword ? 'password' : 'text'"
        label="Введите пароль"
      >
        <template #append>
          <q-icon
            :name="isPassword ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPassword = !isPassword"
          />
        </template>
      </q-input>
      <label class="form__upload">
        <q-icon size="sm" name="cloud_upload" />
        Загрузить фото
        <input
          accept=".jpg, .jpeg, .png, .svg, .webp, .avif"
          type="file"
          hidden
          @change="onSelectAvatar($event.target as HTMLInputElement)"
        />
      </label>
      <q-avatar class="form__avatar" size="150px">
        <q-img
          v-if="previewAvatar || form.image"
          :src="previewAvatar || form.image"
          alt="Avatar image"
        />
        <svg
          v-else
          width="1em"
          height="1em"
          viewBox="0 0 200 200"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M100.002 110.75C123.013 110.75 141.668 92.0955 141.668 69.0837C141.668 46.0718 123.013 27.417 100.002 27.417C76.9898 27.417 58.335 46.0718 58.335 69.0837C58.335 92.0955 76.9898 110.75 100.002 110.75Z"
            fill="#9DA3AC"
            fill-opacity="0.5"
          />
          <path
            d="M102.002 121C52.398 121 12.002 154.18 12.002 195.062C12.002 197.827 14.1802 200 16.9524 200H187.051C189.824 200 192.002 197.827 192.002 195.062C192.002 154.18 151.606 121 102.002 121Z"
            fill="#9DA3AC"
            fill-opacity="0.5"
          />
        </svg>
      </q-avatar>
      <q-btn padding="10px" color="primary" type="submit">Зарегистрироваться</q-btn>
      <div class="text-center">
        Уже есть аккаут?
        <router-link to="/login">Авторизоваться</router-link>
      </div>
    </q-form>
  </div>
</template>

<style scoped lang="scss">
.container {
  max-width: 400px;
  margin: 0 auto;
  display: grid;
  place-items: center;
  height: 100vh;
}

.form {
  width: 100%;
  display: grid;
  gap: 20px;
  padding: 20px;
  border: 1px solid $grey-9;
  border-radius: 10px;

  &__upload {
    justify-self: center;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 10px;
    cursor: pointer;
    border: 1px solid $grey-8;
    border-radius: 10px;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: $grey-10;
    }
  }

  &__avatar {
    border: 2px dashed $dark;
    justify-self: center;
  }
}
</style>
