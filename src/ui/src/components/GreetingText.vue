<template>
  <div class="container">
    <h5 class="title">Hello! 👋</h5>
    <p class="text">
      I am AirAI. An assistant that helps you with information about air quality. 
      <br /><br />
      I'm capable of
      obtaining real-time readings of various pollution measurement stations throughout the world
      and present them in a simple yet comprehensive way. 
      <br /><br />
      I also contextualize my responses with
      facts about the places you ask me about, that could help you better understand the
      implications of its air quality, or what affects it. 
      
      Ask me anything.
    </p>
  </div>
</template>

<style scoped lang="scss">
.container {
  margin: 0 auto;
  width: 100%;
  max-width: 500px;
  margin-top: 1rem;
}

.title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: $gray800;
}

.text {
  font-size: 1rem;
  line-height: 1.1rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  color: $gray600;
}
</style>
