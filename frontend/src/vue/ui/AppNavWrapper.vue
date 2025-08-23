<template>
  <nav>
    <slot/>
  </nav>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";

@Component({name: "AppNavWrapper"})
export default class AppNavWrapper extends Vue {

}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>

@import "@/assets/sass/partials/apple-mixins"

nav
  @include apple-navbar
  height: $apple-nav-height
  background: rgba($apple-background-elevated, 0.95)
  backdrop-filter: $apple-blur-light
  border-bottom: 1px solid $apple-fill-primary
  padding: 0 $apple-spacing-lg
  box-shadow: $apple-shadow-sm

</style>
