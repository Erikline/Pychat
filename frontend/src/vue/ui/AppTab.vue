<template>
  <div class="links">
    <slot/>
  </div>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";

@Component({name: "AppTab"})
export default class AppTab extends Vue {

}
</script>
<!-- eslint-disable -->
<style
  lang="sass"
  scoped
>
@import "@/assets/sass/partials/variables"
@import "@/assets/sass/partials/abstract_classes"
.links
  display: flex
  margin-top: 20px
  padding: 12px
  justify-content: space-between
  background: #FFFFFF
  border-radius: 12px
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08)

  :deep(a)
    padding: 12px 20px
    color: $link-color
    font-weight: 500
    border-radius: 8px
    transition: all 0.3s ease
    text-decoration: none

    &:hover
      cursor: pointer
      background: rgba(52, 152, 219, 0.1)
      color: #2980B9
      transform: translateY(-1px)

    &.router-link-active
      color: #FFFFFF
      background: linear-gradient(135deg, $active-color 0%, lighten($active-color, 10%) 100%)
      box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3)

@media screen and (max-width: $collapse-width)
  .links
    flex-direction: column
    padding: 0

    a
      text-align: center
      padding: 4px

.color-white .links :deep(a)
  color: #c3fffd

  &.router-link-active
    color: #e8e156
</style>
