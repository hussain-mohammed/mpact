<template>
<div
        class="toast position-absolute mx-auto"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        data-delay="2000"
      >
        <div class="toast-body">{{text}}</div>
      </div>
</template>

<script>

export default {
    props:["text"]
}
</script>

<style scoped>
</style>