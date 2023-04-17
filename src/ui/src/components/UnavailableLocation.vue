<template>
  <div class="container">
    <p class="title">Where are you?</p>
    <p class="text">
      In order to answer this, please enable your browser`s location functionality. 
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
  max-width: 400px;
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
  line-height: 1.1rem;
}

</style>
