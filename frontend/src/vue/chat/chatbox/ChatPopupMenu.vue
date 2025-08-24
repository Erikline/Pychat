<template>
  <app-modal>
    <div class="popup-menu">
      <div class="menu-item" @click="invertSearch">
        <i class="icon-search menu-icon" title="在当前房间搜索消息 (Shift+Ctrl+F)"></i>
        <span class="menu-text">搜索</span>
      </div>
      
      <div class="menu-item" @click="startCall">
        <i class="icon-phone menu-icon" title="发起视频/语音通话"></i>
        <span class="menu-text">通话</span>
      </div>
      
      <router-link v-if="activeRoom && activeRoom.name" 
                   :to="`/room-users/${activeRoomId}`" 
                   class="menu-item menu-link">
        <i class="icon-user-pair menu-icon"></i>
        <span class="menu-text">用户</span>
      </router-link>
      
      <router-link v-if="activeRoom && activeRoom.isMainInChannel" 
                   :to="`/channel/${activeRoom.channelId}/room`" 
                   class="menu-item menu-link">
        <i class="icon-plus-squared menu-icon"></i>
        <span class="menu-text">添加房间</span>
      </router-link>
      
      <router-link v-if="activeRoom && activeRoom.isMainInChannel" 
                   :to="`/channel/${activeRoom.channelId}/settings`" 
                   class="menu-item menu-link">
        <i class="icon-cog menu-icon"></i>
        <span class="menu-text">设置</span>
      </router-link>
      
      <router-link v-else-if="activeRoom" 
                   :to="`/room-settings/${activeRoomId}`" 
                   class="menu-item menu-link">
        <i class="icon-cog menu-icon"></i>
        <span class="menu-text">设置</span>
      </router-link>
    </div>
  </app-modal>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import {State} from "@/ts/instances/storeInstance";
import {RoomModel} from "@/ts/types/model";
import AppModal from "@/vue/ui/AppModal.vue";

@Component({
  name: "ChatPopupMenu",
  components: {
    AppModal,
  },
})
export default class ChatPopupMenu extends Vue {
  @State
  public readonly activeRoomId!: number;

  @State
  public readonly activeRoom!: RoomModel;

  public invertSearch() {
    this.$store.toogleSearch(this.activeRoomId);
  }

  public startCall() {
    this.$webrtcApi.startCall(this.activeRoomId);
  }
}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>
@import "@/assets/sass/partials/mixins"

.popup-menu
  display: flex
  flex-direction: column
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)
  padding: 8px 0
  border-radius: 12px
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08)
  border: 1px solid rgba(255, 255, 255, 0.2)
  backdrop-filter: blur(10px)
  margin-left: auto
  margin-top: 51px
  align-self: flex-start
  min-width: 180px
  overflow: hidden

.menu-item
  display: flex
  align-items: center
  padding: 12px 16px
  cursor: pointer
  transition: all 0.2s ease
  color: #374151
  text-decoration: none
  border-bottom: 1px solid rgba(0, 0, 0, 0.05)
  
  &:last-child
    border-bottom: none

  &:hover
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.1) 100%)
    transform: translateX(2px)
    color: #3b82f6

  &:active
    transform: translateX(0)

.menu-link
  &:hover
    color: #3b82f6

.menu-icon
  font-size: 18px
  margin-right: 12px
  width: 20px
  text-align: center
  color: #6b7280
  transition: color 0.2s ease

.menu-item:hover .menu-icon
  color: #3b82f6

.menu-text
  font-size: 14px
  font-weight: 500
  letter-spacing: 0.3px

// 清新主题色彩变量
:root
  --fresh-primary: #3b82f6
  --fresh-secondary: #60a5fa
  --fresh-accent: #93c5fd
  --fresh-bg: #f8fafc
  --fresh-text: #374151
  --fresh-muted: #6b7280
</style>
