<template>
  <div :class="['toast', 'position-absolute', 'mx-auto', { 'bg-danger text-white': hasError }]" aria-live='assertive'
    aria-atomic='true' role='alert' data-delay='2000'>
    <div class='toast-body'>{{ text }}</div>
  </div>
</template>

<script>
export default {
  props: ['text', 'hasError'],
};
</script>
