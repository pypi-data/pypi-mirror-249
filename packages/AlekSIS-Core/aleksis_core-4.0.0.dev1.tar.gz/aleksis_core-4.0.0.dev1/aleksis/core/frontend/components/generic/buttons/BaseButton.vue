<template>
  <v-btn v-bind="{ ...$props, ...$attrs }" @click="$emit('click', $event)">
    <slot>
      <v-icon v-if="iconText" left>{{ iconText }}</v-icon>
      <span v-t="i18nKey" />
    </slot>
  </v-btn>
</template>

<script>
export default {
  name: "BaseButton",
  inheritAttrs: true,
  extends: "v-btn",
  props: {
    i18nKey: {
      type: String,
      required: true,
    },
    iconText: {
      type: String,
      required: false,
      default: undefined,
    },
  },
};
</script>

<style scoped></style>
