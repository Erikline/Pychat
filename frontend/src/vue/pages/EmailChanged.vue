<template>
  <div>
    <div class="message">
      {{ message }}<br/>
      <router-link to="/">
        返回主页
      </router-link>
    </div>
    <div v-if="loading" class="spinner"/>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import {ApplyGrowlErr} from "@/ts/instances/storeInstance";

@Component({name: "ConfirmMail"})
export default class ConfirmMail extends Vue {
  public loading!: boolean;

  public message: string | null = null;

  @ApplyGrowlErr({
    runningProp: "loading",
    vueProperty: "message",
    message: "更改邮箱时出错",
  })
  public async created() {
    this.message = await this.$api.changeEmail(<string> this.$route.query.token);
  }
}
</script>
<style lang="sass" scoped>

@import "@/assets/sass/partials/mixins"

.spinner
  @include lds-30-spinner-vertical('正在更改邮箱...')

.message
  text-align: center
  font-size: 30px
  font-family: monospace
  display: table
  width: 100%
  vertical-align: middle
  margin-top: 15%
</style>re

