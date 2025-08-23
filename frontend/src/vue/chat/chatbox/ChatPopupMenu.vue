<template>
  <app-modal>
    <div class="popup-menu">
      <i
          class="icon-search"
          title="在当前房间搜索消息 (Shift+Ctrl+F)"
          @click="invertSearch"
        >
          <span class="mText">搜索</span>
        </i>
        <i
          class="icon-phone"
          title="发起视频/语音通话"
          @click="startCall"
        ><span class="mText">通话</span></i>
      <router-link v-if="activeRoom && activeRoom.name" :to="`/room-users/${activeRoomId}`">
        <i class="icon-user-pair"/> 用户
      </router-link>
      <router-link v-if="activeRoom && activeRoom.isMainInChannel" :to="`/channel/${activeRoom.channelId}/room`">
        <i class="icon-plus-squared"/> 添加房间
      </router-link>
      <router-link v-if="activeRoom && activeRoom.isMainInChannel" :to="`/channel/${activeRoom.channelId}/settings`">
        <i class="icon-cog"/> 设置
      </router-link>
      <router-link v-else-if="activeRoom" :to="`/room-settings/${activeRoomId}`">
        <i class="icon-cog"/> 设置
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

.popup-menu
  display: flex
  flex-direction: column
  background-color: #f8fafc
  padding: 5px 10px
  font-size: 26px
  border: 1px #696951 solid
  margin-left: auto
  margin-top: 51px
  align-self: flex-start

  > *
    padding: 5px
</style>
