<template>
  <div
    v-if="checkingToken"
    class="spinner"
  />
  <h1
    v-else-if="error"
    class="error"
  >
    {{ error }}
  </h1>
  <form
    v-else
    method="post"
    @submit.prevent="submitResetPassword"
  >
    <div class="restoreHeader">
        重置密码
        <b>{{ restoreUser }}</b>
      </div>
    <input
      v-model="password"
      class="input"
      placeholder="密码"
      required
      type="password"
    />
    <input
      v-model="repeatPassword"
      class="input"
      placeholder="重复密码"
      required
      type="password"
    />
    <app-submit
      :running="running"
      class="submit-button"
      value="提交密码"
    />
  </form>
</template>
<script lang="ts">

import {
  Component,
  Vue,
} from "vue-property-decorator";
import {ApplyGrowlErr} from "@/ts/instances/storeInstance";
import AppSubmit from "@/vue/ui/AppSubmit.vue";

@Component({
  name: "ApplyResetPassword",
  components: {AppSubmit},
})
export default class ApplyResetPassword extends Vue {
  restoreUser: string = "";

  error: string | null = null;

  checkingToken: boolean = false;

  running: boolean = false;

  password: string = "";

  repeatPassword: string = "";

  @ApplyGrowlErr({
    runningProp: "checkingToken",
    vueProperty: "error",
  })
  async created() {
    this.restoreUser = await this.$api.verifyToken((this.$route.query.token) as string);
  }

  @ApplyGrowlErr({
    runningProp: "running",
    vueProperty: "error",
    message: "重置密码错误",
  })
  async submitResetPassword() {
    if (this.password !== this.repeatPassword) {
      this.$store.growlError("密码不匹配");
    } else {
      await this.$api.acceptToken(this.$route.query.token as string, this.password);
      this.$store.growlSuccess("密码已重置");
      this.$router.replace("/auth/login");
    }
  }
}
</script>
<style lang="sass" scoped>

$restPassMargin: 20px

@import "@/assets/sass/partials/mixins"

.spinner
  @include lds-30-spinner-vertical('Checking token...')

.restoreHeader
  font-size: 25px
  text-align: center
  width: 100%
  margin-left: $restPassMargin
  margin-right: $restPassMargin

.error
  color: red
</style>
