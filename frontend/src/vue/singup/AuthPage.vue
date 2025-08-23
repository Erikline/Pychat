<template>
  <div class="auth-wrapper">
    <div class="reg-log-container">
      <div class="card">
        <div class="topBtns">
          <router-link to="/auth/sign-up">
            注册
          </router-link>
          <router-link to="/auth/login">
            登录
          </router-link>
        </div>
        <h1>{{ regHeader }}</h1>
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import {
  Component,
  Vue,
} from "vue-property-decorator";
import {
  ApplyGrowlErr,
  State,
} from "@/ts/instances/storeInstance";
import {AUTO_REGISTRATION} from "@/ts/utils/consts";
import type {LoginMessage} from "@/ts/types/messages/innerMessages";

@Component({name: "AuthPage"})
export default class AuthPage extends Vue {
  @State
  public readonly regHeader!: string;

  public getRandom(): string {
    return Math.random().toString(36).
      substring(7);
  }

  @ApplyGrowlErr({message: "自动注册失败"})
  public async created() {
    if (AUTO_REGISTRATION) {
      const {session} = await this.$api.registerDict(this.getRandom(), this.getRandom());
      const message: LoginMessage = {
        action: "login",
        handler: "router",
        session,
      };
      this.$messageBus.notify(message);
    }
  }
}
</script>

<style lang="sass" scoped>

@import "@/assets/sass/partials/mixins"
@import "@/assets/sass/partials/variables"

// Layout wrapper
.auth-wrapper
  min-height: 100vh
  display: flex
  align-items: center
  justify-content: center
  padding: 24px
  background: #ffffff
  position: relative
  overflow: hidden
  
  &::before
    content: ''
    position: absolute
    top: 0
    left: 0
    right: 0
    bottom: 0
    background: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><circle cx='80' cy='80' r='3' fill='%23e3f2fd' opacity='0.6'/><circle cx='320' cy='120' r='2' fill='%23bbdefb' opacity='0.5'/><circle cx='150' cy='200' r='4' fill='%23e1f5fe' opacity='0.4'/><circle cx='280' cy='280' r='2.5' fill='%23b3e5fc' opacity='0.6'/><circle cx='50' cy='300' r='3.5' fill='%23e0f2f1' opacity='0.5'/><circle cx='350' cy='50' r='2' fill='%23f1f8e9' opacity='0.4'/><circle cx='200' cy='350' r='3' fill='%23e8f5e8' opacity='0.6'/><circle cx='120' cy='120' r='1.5' fill='%23e3f2fd' opacity='0.3'/></svg>") no-repeat
    background-size: 100% 100%
    pointer-events: none
    z-index: 0
    animation: floatBackground 20s ease-in-out infinite

// Card container
.reg-log-container
  overflow-y: visible
  padding: 0
  max-width: 440px
  width: 100%
  margin: 0 auto
  position: relative
  z-index: 1

.card
  background: rgba(255, 255, 255, 0.95)
  backdrop-filter: blur(20px)
  border-radius: 24px
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.2)
  padding: 40px 32px 32px
  border: 1px solid rgba(255, 255, 255, 0.2)
  transition: all 0.3s ease
  
  &:hover
    transform: translateY(-2px)
    box-shadow: 0 35px 60px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(255, 255, 255, 0.3)

.brand
  display: flex
  align-items: center
  justify-content: center
  gap: 12px
  margin-bottom: 24px

.logo
  font-size: 36px
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))
  animation: float 3s ease-in-out infinite
  
@keyframes float
  0%, 100%
    transform: translateY(0px)
  50%
    transform: translateY(-5px)

@keyframes floatBackground
  0%, 100%
    transform: translateY(0px) translateX(0px)
    opacity: 0.8
  25%
    transform: translateY(-10px) translateX(5px)
    opacity: 0.6
  50%
    transform: translateY(-5px) translateX(-3px)
    opacity: 0.9
  75%
    transform: translateY(-15px) translateX(8px)
    opacity: 0.7

.title
  font-weight: 700
  font-size: 24px
  color: #1a202c
  font-family: $apple-font-family
  letter-spacing: -0.5px

h1
  text-align: center
  color: #2d3748
  font-weight: 600
  font-size: 20px
  margin: 0 0 24px 0
  font-family: $apple-font-family
  width: 100%

%top-btn-register
  border-top: 1px solid rgba(255, 255, 255, 0.6)
  border-left: 1px solid rgba(171, 171, 171, 0.83)
  text-transform: uppercase
  font: 14px Oswald
  border-radius: 0

%cyan-btn
  @include linear-gradient-hover(#BABDB6, #28D2DE, 15px, 12px)
  @extend %top-btn-register
  border-radius: 0

// Tabs (register/login)
.topBtns
  display: flex
  gap: 4px
  margin-bottom: 24px
  background: rgba(241, 245, 249, 0.8)
  padding: 4px
  border-radius: 16px
  backdrop-filter: blur(10px)
  border: 1px solid rgba(255, 255, 255, 0.2)

  > *
    flex: 1
    text-align: center
    padding: 12px 16px
    border-radius: 12px
    color: #64748b
    text-decoration: none
    font-weight: 600
    font-size: 15px
    transition: all .3s cubic-bezier(0.4, 0, 0.2, 1)
    position: relative
    font-family: $apple-font-family

    &:hover
      background: rgba(255, 255, 255, 0.6)
      color: #334155
      transform: translateY(-1px)

  .router-link-active
    background: linear-gradient(135deg, #4dd0e1 0%, #26c6da 100%)
    color: #ffffff
    box-shadow: 0 4px 12px rgba(77, 208, 225, 0.4)
    transform: translateY(-1px)
    
    &:hover
      transform: translateY(-2px)
      box-shadow: 0 6px 16px rgba(77, 208, 225, 0.5)

.reg-log-container :deep(.submit-button)
  @extend %cyan-btn
  width: 100%
  border-radius: 5px

  &:active
    border-bottom-color: rgba(0, 0, 0, 0)


.reg-log-container :deep(form)
  margin: auto
  text-align: center

  > *
    margin: auto
    position: relative
    width: 100%

.reg-log-container :deep(select.input)
  -webkit-appearance: none
// paddings don't work on devices like macos chrome, but work on windows

.reg-log-container
  :deep(.input)
    border-radius: 5px
    margin-bottom: 10px
    font-size: 16px
    width: calc(100% - 58px)
    padding: 15px 22px 15px 35px
    border: 2px solid rgba(226, 232, 240, 0.8)
    
    &::placeholder
      color: rgba(100, 116, 139, 0.7)
  
  :deep(select.input)
    width: calc(100% - 58px)
    padding: 15px 22px 15px 35px
    font-weight: 500
    font-size: 16px
    border: 2px solid rgba(226, 232, 240, 0.8)
    
    &::placeholder
      color: rgba(100, 116, 139, 0.7)


.reg-log-container :deep(input:-webkit-autofill)
  -webkit-box-shadow: 0 0 0 1000px #242400 inset !important
  -webkit-text-fill-color: #C6C6B6 !important
  color: #C6C6B6


.color-reg

  .reg-log-container ::deep(select)
    color: #79797a

  .reg-log-container :deep(.submit-button)
    border: 1px solid #e5e7eb

  .reg-log-container :deep(.reg-log-container)
    input[type=button], input[type=submit]
      &:active
        padding-top: $register-buttons-vertical-pad + 1
        padding-bottom: $register-buttons-vertical-pad - 1

    [class^='icon-']
      position: absolute
      top: 12px
      left: 5px
      color: #a0aec0
      font-size: 18px
      transition: all 0.3s ease
      z-index: 1
      opacity: 1
      text-shadow: none
      cursor: auto
      
      &.error
        color: #e53e3e
      
      &.success
        color: #38a169
      
      &.warn
        color: #d69e2e

.router-link-active
  @extend %cyan-btn


</style>

.reg-log-container :deep(select.input)
  color: #2d3748
  
  option[disabled][selected]
    color: rgba(100, 116, 139, 0.7)
