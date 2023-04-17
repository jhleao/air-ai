<template>
  <div class="link-container">
    <GithubIcon />
    <a class="link" target="_blank" :href="url">View on GitHub</a>
  </div>
</template>

<script lang="ts">
import GithubIcon from './Icons/GithubIcon.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  components: { GithubIcon },
  data() {
    return {
      url: 'https://www.github.com/jhleao/air-ai'
    };
  }
});
</script>

<style lang="scss">
.link-container {
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: flex-end;
  gap: 0.4rem;
  margin-top: 1rem;
  flex: 1;
}


.link {
  font-size: 0.8rem;
  color: $gray600;
  text-decoration: underline;
  cursor: pointer;
}
</style>
