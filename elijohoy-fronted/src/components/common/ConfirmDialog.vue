<template>
  <q-dialog v-model="show" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <q-icon :name="icon" color="primary" size="32px" class="q-mr-md" />
        <div>
          <div class="text-h6">{{ title }}</div>
          <div>{{ message }}</div>
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Cancelar" color="primary" v-close-popup @click="cancel" />
        <q-btn flat label="Aceptar" color="primary" @click="ok" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  props: {
    modelValue: Boolean,
    title: {
      type: String,
      default: 'Confirmar'
    },
    message: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: 'help_outline'
    }
  },
  emits: ['update:modelValue', 'ok', 'cancel'],
  data() {
    return {
      show: this.modelValue
    }
  },
  watch: {
    modelValue(val) {
      this.show = val
    },
    show(val) {
      this.$emit('update:modelValue', val)
    }
  },
  methods: {
    ok() {
      this.$emit('ok')
      this.show = false
    },
    cancel() {
      this.$emit('cancel')
      this.show = false
    }
  }
}
</script>

<style scoped>
.q-card-section {
  min-width: 250px;
}
</style>
