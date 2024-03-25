<script setup lang="ts">
import { computed, watch } from 'vue'
import { useChatStore } from 'stores/chat'
import { storeToRefs } from 'pinia'
import { useRoute } from 'vue-router'

const props = defineProps<{ file: File }>()

const route = useRoute()
const id = computed(() => route.params.id as string)

const store = useChatStore()
const { message } = storeToRefs(store)

const isOpen = defineModel<boolean>('isOpen', { required: true })

async function onSend() {
  await store.sendMessage(id.value)
  isOpen.value = false
}

watch(
  () => props.file,
  () => {
    console.log(props.file)
  }
)
</script>

<template>
  <q-dialog v-model="isOpen">
    <div class="dialog bg-dark">
      <div class="content">
        {{ file.name }}
      </div>
      <div class="actions">
        <q-input
          v-model="message"
          borderless
          class="full-width"
          label="Введите надпись"
          @keyup.enter="onSend"
        />
        <q-btn rounded flat icon="send" @click="onSend" />
      </div>
    </div>
  </q-dialog>
</template>

<style scoped lang="scss">
.dialog {
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.content {
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
