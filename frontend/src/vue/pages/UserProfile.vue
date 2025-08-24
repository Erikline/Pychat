<template>
  <div class="holder">
    <app-tab class="tab">
      <router-link to="/profile/user-info">
        用户信息
      </router-link>
      <router-link to="/profile/image">
        头像
      </router-link>
      <router-link to="/profile/change-password">
        修改密码
      </router-link>
      <router-link to="/profile/change-email">
        修改邮箱
      </router-link>
      <router-link v-if="GOOGLE_OAUTH_2_CLIENT_ID && FACEBOOK_APP_ID" to="/profile/oauth-settings">
        社交账户
      </router-link>
    </app-tab>
    <div class="container">
      <router-view v-slot="{Component, route}">
        <keep-alive>
          <component
            :is="Component"
            :key="route.meta.usePathKey ? route.path : undefined"
            class="profileInner"
          />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>
<script lang="ts">
import {
  FACEBOOK_APP_ID,
  GOOGLE_OAUTH_2_CLIENT_ID,
} from "@/ts/utils/consts";
import {
  Component,
  Vue,
} from "vue-property-decorator";
import AppTab from "@/vue/ui/AppTab.vue";

@Component({
  name: "UserProfile",
  components: {AppTab},
})
export default class UserProfile extends Vue {
  public readonly GOOGLE_OAUTH_2_CLIENT_ID = GOOGLE_OAUTH_2_CLIENT_ID;

  public readonly FACEBOOK_APP_ID = FACEBOOK_APP_ID;
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/partials/variables"
@import "@/assets/sass/partials/abstract_classes"

.holder
  @extend %room-settings-holder
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)
  border-radius: 16px
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04)
  border: 1px solid rgba(255, 255, 255, 0.2)
  backdrop-filter: blur(10px)
  padding: 32px
  margin: 20px auto
  max-width: 700px
  width: 100%

.tab
  max-width: 680px
  margin-bottom: 24px
  
  :deep(a)
    padding: 12px 20px
    margin-right: 8px
    border-radius: 8px
    background: rgba(59, 130, 246, 0.1)
    color: #3b82f6
    text-decoration: none
    font-weight: 500
    transition: all 0.2s ease
    
    &:hover
      background: rgba(59, 130, 246, 0.2)
      transform: translateY(-1px)
    
    &.router-link-active
      background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)
      color: white
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3)

.profileInner
  :deep(button)
    width: 100%
    background: linear-gradient(135deg, #10b981 0%, #34d399 100%)
    border: none
    border-radius: 8px
    padding: 12px 24px
    font-weight: 600
    color: white
    transition: all 0.2s ease
    cursor: pointer
    
    &:hover
      transform: translateY(-1px)
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3)

  padding-top: 10px
  padding-bottom: 10px

  :deep(table)
    margin: auto
    width: 100%
    border-collapse: collapse

  :deep(th)
    text-align: right
    font-weight: 600
    color: #374151
    padding: 12px 16px
    background: rgba(248, 250, 252, 0.5)

  :deep(td), :deep(th)
    padding: 12px 16px
    border-bottom: 1px solid rgba(0, 0, 0, 0.05)

  :deep(.input)
    @extend %big-input
    border: 1px solid #d1d5db
    transition: all 0.2s ease
    
    &:focus
      outline: none
      border-color: #3b82f6
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1)

  :deep(.container)
    background: rgba(248, 250, 252, 0.3)
    border-radius: 12px
    padding: 24px
    margin-top: 16px
</style>
