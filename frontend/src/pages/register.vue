<script setup lang="ts">
import { reactive, ref } from 'vue'
import AuthService from 'src/api/auth'
import { Register } from 'src/api/auth/types'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import PersonIcon from 'src/icons/person.vue'

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
    const { data } = await AuthService.register(formData)
    $q.localStorage.set('id_access', data.id)
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
        <img
          v-if="previewAvatar || form.image"
          :src="previewAvatar || form.image"
          alt="Avatar image"
        />
        <person-icon v-else />
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
