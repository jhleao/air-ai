<template>
  <div class="container">
    <input
      :value="value"
      @input="onChange"
      @keypress="onKeypress"
      class="input"
      v-bind="{ ...$attrs }"
    />
    <div class="divider"></div>
    <button @click="submit" class="send" :class="{ disabled: submitDisabled }" type="button">
      Send
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    value: {
      type: String,
      required: true
    },
    submitDisabled: {
      type: Boolean,
      required: false
    }
  },
  methods: {
    onChange(e: Event) {
      this.$emit('update', e?.target?.value ?? '')
    },
    onKeypress(e: KeyboardEvent) {
      if (e?.key === 'Enter') {
        this.submit()
      }
    },
    submit() {
      if (this.submitDisabled) return
      this.$emit('submit')
    }
  }
})
</script>

<style scoped lang="scss">
$height: 40px;
$radius: 0.5rem;
$border-thickness: 1px;

.container {
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  width: 100%;
  max-width: 500px;
  margin-top: 1rem;
  border: solid $border-thickness $gray300;
  border-radius: $radius;
  background: none;
  height: $height;
}

.divider {
  height: $height;
  width: $border-thickness;
  background-color: $gray300;
}

.input {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  font-size: 1.1rem;
  color: $gray500;
  margin: 0;
  background: none;
  padding: 0.5rem;
  padding-left: 1rem;

  &::placeholder {
    color: $gray400;
    font-size: 1.05rem;
  }
}

.send {
  font-size: 1.1rem;
  color: $gray500;
  padding-left: 1rem;
  padding-right: 1rem;
  background: none;
  border: none;
  height: calc($height - $border-thickness * 2);
  border-top-right-radius: $radius;
  border-bottom-right-radius: $radius;
  transition: background-color 0.1s ease-out;
  z-index: 1;

  &:hover {
    background-color: $gray75;
    cursor: pointer;
  }
}

.disabled {
  color: $gray300;
  background-color: $gray75;
  cursor: pointer;
}
</style>
