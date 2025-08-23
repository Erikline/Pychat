<template>
  <app-nav-wrapper>
    <i
      v-if="lowWidth && currentPage === 'chat'"
      class="icon-left"
      @click="goBack"
    />
    <i
      v-else
      class="icon-menu"
      @click="showMenu"
    />
    <template v-if="lowWidth">
      <user-nav-info v-if="user" :user="user"/>
      <span
        v-else
        class="room-name"
      >{{ roomName }}</span>
    </template>
    <div class="chat-right-icons">
      <chat-is-online-icon/>
      <i
        v-if="!lowWidth || currentPage === 'chat'"
        class="icon-chat"
        @click="showPopupToggle"
      />
    </div>
  </app-nav-wrapper>
</template>
<script lang="ts">
import {
  Component,
  Emit,
  Prop,
  Vue,
} from "vue-property-decorator";
import AppNavWrapper from "@/vue/ui/AppNavWrapper.vue";
import {State} from "@/ts/instances/storeInstance";
import type {UserModel} from "@/ts/types/model";
import {
  ChannelsDictUIModel,
  RoomModel,
  UserDictModel,
} from "@/ts/types/model";
import ChatIsOnlineIcon from "@/vue/chat/chatbox/ChatIsOnlineIcon.vue";
import {PrivateRoomsIds} from "@/ts/types/types";
import UserNavInfo from "@/vue/chat/right/UserNavInfo.vue";

@Component({
  name: "ChatNavBar",
  components: {
    UserNavInfo,
    ChatIsOnlineIcon,
    AppNavWrapper,
  },
})
export default class ChatNavBar extends Vue {
  @State
  public readonly activeRoom!: RoomModel;

  @Prop()
  public readonly lowWidth!: boolean;

  @Prop()
  public readonly currentPage!: string;

  @State
  public readonly privateRoomsUsersIds!: PrivateRoomsIds;

  @State
  public readonly channelsDictUI!: ChannelsDictUIModel;

  @State
  public readonly allUsersDict!: UserDictModel;

  public get roomName(): string {
    if (this.activeRoom.name) {
      return this.activeRoom.name;
    }
    if (this.activeRoom.isMainInChannel) {
      return this.channelsDictUI[this.activeRoom.channelId!].name;
    }
    if (this.user) {
      return this.user.user;
    }
    throw Error("Invalid structure");
  }

  public get user(): UserModel | null {
    if (!this.activeRoom || !this.activeRoom.name) {
      if (this.activeRoom && this.activeRoom.id) {
        return this.allUsersDict[this.privateRoomsUsersIds.roomUsers[this.activeRoom.id]];
      }
      return null;
    }
    return null;
  }

  @Emit()
  goBack() {
  }

  @Emit()
  showPopupToggle(e: Event) {
    e.stopPropagation();
  }

  @Emit()
  showMenu(e: Event) {
    e.stopPropagation();
  }
}
</script>
<!-- eslint-disable -->
<style
  lang="sass"
  scoped
>
@import "@/assets/sass/partials/apple-mixins"

.room-name
  margin-left: $apple-spacing-md
  font-weight: $apple-font-weight-semibold
  font-size: $apple-font-size-lg
  color: $apple-label-primary

.chat-right-icons
  margin-left: auto
  display: flex
  align-items: center
  gap: $apple-spacing-md

.icon-chat
  margin-right: $apple-spacing-lg
  color: $apple-label-secondary
  transition: color 0.2s ease
  
  &:hover
    color: $apple-blue

.icon-menu, .icon-chat
  cursor: pointer
  font-size: $apple-font-size-lg
  padding: $apple-spacing-sm
  border-radius: $apple-radius-md
  transition: background-color 0.2s ease
  
  &:hover
    background: $apple-fill-primary

</style>
