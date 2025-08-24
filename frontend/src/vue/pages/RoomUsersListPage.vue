<template>
  <div class="current-room-users-table">
    <div class="current-room-users-table-header">
      {{ title }} <b>{{ room.name }}</b>
    </div>
    <ul :class="ulClass">
      <li v-for="user in usersArray" :key="user.id">
        <user-flag-row :user="user"/>
      </li>
    </ul>
    <template v-if="showInviteUsers">
      <div class="current-room-users-table-header">
        邀请更多用户
      </div>
      <div class="holder">
        <pick-user
          v-model="userdToAdd"
          :users-ids="userIds"
        />
        <app-submit
          :running="running"
          class="green-btn"
          type="button"
          value="应用"
          @click.native="add"
        />
      </div>
    </template>
  </div>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import {
  ApplyGrowlErr,
  State,
} from "@/ts/instances/storeInstance";
import {
  ChannelsDictUIModel,
  RoomDictModel,
  UserDictModel,
} from "@/ts/types/model";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import PickUser from "@/vue/parts/PickUser.vue";
import UserFlagRow from "@/vue/chat/right/UserFlagRow.vue";

@Component({
  name: "RoomUsersListPage",
  components: {
    UserFlagRow,
    AppSubmit,
    PickUser,
  },
})
export default class RoomUsersListPage extends Vue {
  @State
  public readonly allUsersDict!: UserDictModel;

  @State
  public readonly roomsDict!: RoomDictModel;

  @State
  public readonly channelsDictUI!: ChannelsDictUIModel;


  public userdToAdd: number[] = [];

  public running: boolean = false;

  get showInviteUsers() {
    return this.userIds.length > 0;
  }

  get ulClass() {
    return {
      "current-room-users-table-header-single": !this.showInviteUsers,
    };
  }

  public get roomId(): number {
    return parseInt(this.$route.params.id as string);
  }

  public get room() {
    return this.roomsDict[this.roomId];
  }

  public get title() {
    return this.room.isMainInChannel ? "群组成员" : "房间成员";
  }

  public get usersArray() {
    return this.room.users.map((id) => this.allUsersDict[id]);
  }

  public get userIds(): number[] {
    if (this.room.channelId && !this.room.isMainInChannel) {
      return this.channelsDictUI[this.room.channelId].mainRoom.users.filter((uId) => !this.room.users.includes(uId));
    }
    return this.$store.usersArray.filter((u) => !this.room.users.includes(u.id)).map((u) => u.id);
  }

  @ApplyGrowlErr({runningProp: "running"})
  async add() {
    if (this.userdToAdd.length > 0) {
      const e = await this.$ws.inviteUser(this.roomId, this.userdToAdd);
      this.$router.replace(`/chat/${e.roomId}`);
    } else {
      this.$store.growlError("请至少选择一个用户");
    }
  }
}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>
@import "@/assets/sass/partials/room_users_table"
@import "@/assets/sass/partials/abstract_classes"

.current-room-users-table
  font-size: 16px
  max-width: 600px
  width: 100%
  margin: 20px auto
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)
  border-radius: 16px
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04)
  border: 1px solid rgba(255, 255, 255, 0.2)
  backdrop-filter: blur(10px)
  overflow: hidden

.current-room-users-table-header
  font-size: 20px
  font-weight: 600
  padding: 20px 24px
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)
  color: white
  text-align: center
  letter-spacing: 0.5px

  b
    color: #e0f2fe
    font-weight: 700

ul
  overflow-y: auto
  max-height: 400px
  @extend %ul
  margin: 0
  padding: 0

  &.current-room-users-table-header-single
    max-height: 500px

  :deep(li)
    overflow: initial
    border-bottom: 1px solid rgba(0, 0, 0, 0.05)
    transition: all 0.2s ease
    
    &:last-child
      border-bottom: none
    
    &:hover
      background: linear-gradient(90deg, rgba(59, 130, 246, 0.05) 0%, rgba(147, 197, 253, 0.05) 100%)
      transform: translateX(2px)

li
  @extend %li
  justify-content: space-between
  display: flex
  align-items: center
  padding: 12px 24px
  height: 48px

.holder
  @extend %room-settings-holder
  padding: 24px
  background: rgba(248, 250, 252, 0.5)
  border-top: 1px solid rgba(0, 0, 0, 0.05)

.green-btn
  flex-shrink: 0
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

.usersStateText:hover
  cursor: pointer
  color: #3b82f6

// 清新主题样式覆盖
:deep(.user-flag-row)
  display: flex
  align-items: center
  gap: 12px
  
  .user-avatar
    border-radius: 50%
    border: 2px solid rgba(59, 130, 246, 0.2)

  .user-name
    font-weight: 500
    color: #374151
</style>
