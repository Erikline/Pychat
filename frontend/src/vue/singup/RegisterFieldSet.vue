<template>
  <div class="reg-required">
    <i :class="[icon, validation]"/>
    <slot/>
    <div
      :class="{closed}"
      class="slider"
    >
      {{ description }}
    </div>
  </div>
</template>
<script lang="ts">
import {
  Component,
  Prop,
  Vue,
} from "vue-property-decorator";
import {IconColor} from "@/ts/types/types";

@Component({name: "FieldSet"})
export default class FieldSet extends Vue {
  @Prop() public icon!: string;

  @Prop() public validation!: IconColor;

  @Prop() public description!: string;

  @Prop() public closed: boolean = true; // TODO this doesn't work, default should be in decorator
}
</script>
<style lang="sass" scoped>

@import "@/assets/sass/partials/abstract_classes"
.slider
  @extend %slider
  overflow-y: hidden
  height: 30px

  /* approximate max height
  transition: 1s height 0s

  &.closed
    height: 0
    margin: 0
    padding: 0
// Chrome53 pushes block all FORM left if height is set to 0

.reg-required:has(.icon-user-pair)
  i.icon-user-pair
    left: 0px !important  // 性别图标进一步左移，总共左移4px避免偏右

.reg-required
  position: relative

  &:after
    position: absolute
    right: 7px
    top: 17px
    font-size: 17px
    display: inline-block
    font-weight: bold
    color: #6E6E6E

i
  position: absolute
  top: 12px
  left: 5px
  color: #a0aec0
  font-size: 18px
  transition: all 0.3s ease
  z-index: 1
  
  &.error
    color: #e53e3e
  
  &.success
    color: #38a169
  
  &.warn
    color: #d69e2e

.reg-required :deep(.input)
  &::placeholder
    color: rgba(100, 116, 139, 0.7)

.reg-required :deep(select.input)
  color: #2d3748
  
  option[disabled][selected]
    color: rgba(100, 116, 139, 0.7)
</style>
