<template>
  <form
    ref="form"
    @submit.prevent="login"
  >
    <div class="input-group">
      <i class="icon-user"/>
      <input
        autocomplete="username"
        class="input"
        maxlength="254"
        name="username"
        placeholder="用户名/邮箱"
        required
        type="text"
      />
    </div>
    <div class="input-group">
      <i class="icon-key"/>
      <input
        autocomplete="password"
        class="input"
        name="password"
        placeholder="密码"
        required
        type="password"
      />
    </div>
    <router-link
      class="forgot-password"
      to="/auth/reset-password"
    >
      忘记密码？
    </router-link>
    <div class="actions">
      <captcha-component v-model="running"/>
      <app-submit
        :running="running"
        class="submit-button"
        value="登录"
      />
    </div>
  </form>
</template>

<script lang='ts'>
import {
  Component,
  Ref,
  Vue,
} from "vue-property-decorator";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import {ApplyGrowlErr} from "@/ts/instances/storeInstance";

import CaptchaComponent from "@/vue/singup/CaptchaComponent.vue";
import type {LoginMessage} from "@/ts/types/messages/innerMessages";


@Component({
  name: "Login",
  components: {
    CaptchaComponent,
    AppSubmit,
  },
})
export default class Login extends Vue {
  @Ref()
  public form!: HTMLFormElement;

  public running: boolean = false;

  public created() {
    this.$store.setRegHeader("欢迎回来！");
  }

  @ApplyGrowlErr({
    runningProp: "running",
    message: "无法登录",
  })
  public async login() {
    const {session} = await this.$api.login(this.form);
    const message: LoginMessage = {
      action: "login",
      handler: "router",
      session,
    };
    this.$messageBus.notify(message);
  }
}
</script>
<style lang="sass" scoped>

@import "@/assets/sass/partials/abstract_classes"
@import "@/assets/sass/partials/variables"

form
  width: 100%
  max-width: 100%
  margin: 0 auto
  text-align: left

.input-group
  position: relative
  margin-bottom: 20px
  
  .input
    width: 100%
    height: 52px
    padding: 16px 16px 16px 48px
    border: 2px solid rgba(226, 232, 240, 0.8)
    border-radius: 16px
    font-size: 16px
    font-family: $apple-font-family
    background: rgba(255, 255, 255, 0.9)
    backdrop-filter: blur(10px)
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
    color: #2d3748
    box-sizing: border-box
    
    &:focus
      outline: none
      border-color: #667eea
      background: rgba(255, 255, 255, 1)
      box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1)
      transform: translateY(-1px)
    
    &::placeholder
      color: rgba(100, 116, 139, 0.7)
      font-weight: 400
    
    &:hover:not(:focus)
      border-color: rgba(102, 126, 234, 0.3)
      transform: translateY(-1px)

.forgot-password
  display: block
  text-align: center
  margin-top: -8px
  margin-bottom: 20px
  color: #667eea
  font-size: 14px
  text-decoration: none
  transition: all .2s ease
  font-weight: 500
  font-family: $apple-font-family

  &:hover
    color: #5a67d8
    text-decoration: underline
    transform: translateY(-1px)

.actions
  display: flex
  flex-direction: column
  gap: 16px

:deep(.submit-button)
  height: 52px
  border-radius: 16px
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
  border: none
  color: white
  font-size: 16px
  font-weight: 600
  font-family: $apple-font-family
  cursor: pointer
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4)
  
  &:hover:not(:disabled)
    transform: translateY(-2px)
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5)
  
  &:active
    transform: translateY(0)
  
  &:disabled
    opacity: 0.6
    cursor: not-allowed
    transform: none

i
  position: absolute
  top: 18px
  left: 16px
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

.input-group:focus-within i
  color: #667eea
  transform: scale(1.1)
</style>
