<template>
  <app-modal>
    <div class="app-menu-bar">
      <div class="app-header">
        <div class="user-avatar">
          <img v-if="imgSrc" :src="imgSrc" alt="用户头像"/>
        </div>
        <div class="user-info">
          <div class="user-name">{{ userInfo.user }}</div>
          <div class="user-status">在线</div>
        </div>
      </div>
      <div class="app-section">
        <router-link
          class="menu-item"
          title="创建新的私聊房间"
          to="/create-private-room"
        >
          <i class="icon-user menu-icon"></i>
          <span class="menu-text">私聊用户</span>
        </router-link>
        <router-link
          class="menu-item"
          title="创建新的群组房间"
          to="/create-group"
        >
          <i class="icon-users menu-icon"></i>
          <span class="menu-text">创建群组</span>
        </router-link>
        <router-link class="menu-item" title="个人设置" to="/profile">
          <i class="icon-user menu-icon"></i>
          <span class="menu-text">个人资料</span>
        </router-link>
        <router-link class="menu-item" to="/settings">
          <i class="icon-cog menu-icon"></i>
          <span class="menu-text">设置</span>
        </router-link>
        <div class="menu-divider"></div>
        <a
          class="menu-item logout-item"
          href="#"
          title="退出登录"
          @click.prevent="signOut"
        >
          <i class="icon-logout menu-icon"></i>
          <span class="menu-text">退出登录</span>
        </a>
      </div>
    </div>
  </app-modal>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import {
  ISSUES,
} from "@/ts/utils/consts";
import {State} from "@/ts/instances/storeInstance";
import {CurrentUserInfoModel} from "@/ts/types/model";
import AppModal from "@/vue/ui/AppModal.vue";
import {resolveMediaUrl} from "@/ts/utils/htmlApi";

@Component({
  name: "AppMenuBar",
  components: {
    AppModal,
  },
})
export default class AppMenuBar extends Vue {
  @State
  public readonly userInfo!: CurrentUserInfoModel;

  public get imgSrc() {
    return resolveMediaUrl(this.userInfo.image);
  }

  public get consts() {
    return {
      ISSUES,
    };
  }

  public signOut() {
    this.$api.logout(); // 立即退出登录，不等待响应
    const message = {
      action: "logout",
      handler: "*" as const,
    };
    this.$messageBus.notify(message);
    this.$emit("click"); // 关闭菜单
  }
}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>
@import "@/assets/sass/partials/abstract_classes"

.app-menu-bar
  background: white
  border-radius: 12px
  width: 280px
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12)
  overflow: hidden
  border: 1px solid #e5e7eb

.app-header
  padding: 30px 25px
  text-align: center
  background: #f9fafb
  border-bottom: 1px solid #e5e7eb

.user-avatar
  margin-bottom: 15px
  
  img
    border-radius: 50%
    width: 80px
    height: 80px
    border: 3px solid #e5e7eb
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1)

.user-info
  color: #111827

.user-name
  font-size: 18px
  font-weight: 600
  margin-bottom: 5px

.user-status
  font-size: 14px
  color: #6b7280

.app-section
  padding: 10px 0

.menu-item
  display: flex
  align-items: center
  padding: 15px 25px
  color: #374151
  text-decoration: none
  transition: all 0.2s ease
  border-left: 3px solid transparent
  
  &:hover
    background: #f3f4f6
    border-left-color: #3b82f6
    color: #111827

.menu-icon
  font-size: 18px
  margin-right: 15px
  width: 20px
  text-align: center
  color: #6b7280

.menu-text
  font-size: 16px
  font-weight: 500

.menu-divider
  height: 1px
  background: #e5e7eb
  margin: 8px 25px

.logout-item
  color: #ef4444
  
  &:hover
    background: #fef2f2
    border-left-color: #ef4444
    color: #991b1b
</style>
