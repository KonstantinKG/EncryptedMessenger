<script setup lang="ts">
import { reactive, ref } from 'vue'
import EncryptedMessengerService from 'src/api'
import { Register } from 'src/api/types'
import { useRouter } from 'vue-router'

const form = reactive<Register>({
  username: '',
  password: '',
  image: undefined
})
const previewAvatar = ref('')
const isPassword = ref(true)
const router = useRouter()

function onSelectAvatar(file: File) {
  form.image = file
  previewAvatar.value = URL.createObjectURL(file)
}

async function onSubmit() {
  try {
    // const { data } = EncryptedMessengerService.register(form)
    await router.push('/chats')
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <div class="container">
    <q-form class="form" @submit.prevent="onSubmit">
      <q-input v-model="form.username" label="Введите никнейм" />
      <q-input v-model="form.password" :type="isPassword ? 'password' : 'text'" label="Введите пароль">
        <template v-slot:append>
          <q-icon
            :name="isPassword ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPassword = !isPassword"
          />
        </template>
      </q-input>
      <q-file :model-value="form.image" @update:model-value="onSelectAvatar" label="Загрузите аватар">
        <template v-slot:prepend>
          <q-icon name="attach_file" />
        </template>
      </q-file>
      <q-avatar class="form__avatar" size="150px">
        <q-img v-if="previewAvatar || form.image" :src="previewAvatar || form.image" alt="Avatar image" />
        <svg width="1em" height="1em" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M100.002 110.75C123.013 110.75 141.668 92.0955 141.668 69.0837C141.668 46.0718 123.013 27.417 100.002 27.417C76.9898 27.417 58.335 46.0718 58.335 69.0837C58.335 92.0955 76.9898 110.75 100.002 110.75Z"
            fill="#9DA3AC" fill-opacity="0.5" />
          <path
            d="M102.002 121C52.398 121 12.002 154.18 12.002 195.062C12.002 197.827 14.1802 200 16.9524 200H187.051C189.824 200 192.002 197.827 192.002 195.062C192.002 154.18 151.606 121 102.002 121Z"
            fill="#9DA3AC" fill-opacity="0.5" />
        </svg>
        <!--        <q-icon v-else>-->
        <!--          <svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">-->
        <!--            <path-->
        <!--              d="M100.002 110.75C123.013 110.75 141.668 92.0955 141.668 69.0837C141.668 46.0718 123.013 27.417 100.002 27.417C76.9898 27.417 58.335 46.0718 58.335 69.0837C58.335 92.0955 76.9898 110.75 100.002 110.75Z"-->
        <!--              fill="#9DA3AC" fill-opacity="0.5" />-->
        <!--            <path-->
        <!--              d="M102.002 121C52.398 121 12.002 154.18 12.002 195.062C12.002 197.827 14.1802 200 16.9524 200H187.051C189.824 200 192.002 197.827 192.002 195.062C192.002 154.18 151.606 121 102.002 121Z"-->
        <!--              fill="#9DA3AC" fill-opacity="0.5" />-->
        <!--          </svg>-->
        <!--        </q-icon>-->
      </q-avatar>
      <q-btn type="submit">Зарегистрироваться</q-btn>
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

  &__avatar {
    border: 2px dashed $dark;
    justify-self: center;
  }
}
</style>
