<template>
  <div class="container">
    <p class="title">Oopsies...</p>
    <p class="text">
      I ran into issues while trying to resolve your request. Try changing your prompt or
      <span class="link" @click="$emit('tryAgain')">try again</span>.
    </p>
  </div>
</template>

<style scoped lang="scss">
.container {
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  max-width: 350px;
  text-align: center;
  gap: 0.3rem;
  margin-top: 0.5rem;
}

.title {
  font-size: 1.3rem;
  color: $gray700;
  font-weight: 500;
}

.text {
  font-size: 1rem;
  color: $gray500;
}

.link {
  font-size: 1rem;
  color: $gray500;
  text-decoration: underline;
  cursor: pointer;
}
</style>
