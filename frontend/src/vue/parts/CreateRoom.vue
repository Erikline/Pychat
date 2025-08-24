<template>
  <div class="holder">
    <table>
      <tbody>
        <tr v-if="isPublic">
          <th>
            Name
          </th>
          <td>
            <input
              v-model="roomName"
              class="input"
              maxlength="16"
              type="text"
            />
          </td>
        </tr>
        <tr v-if="!isPublic">
          <th>
            Peer to peer
          </th>
          <td>
            <app-checkbox v-model="p2p"/>
          </td>
        </tr>
        <tr v-if="!p2p">
          <th>
            通知
          </th>
          <td>
            <app-checkbox v-model="notifications"/>
          </td>
        </tr>
        <tr>
          <th>
            Sound
          </th>
          <td>
            <app-input-range
              v-model="sound"
              max="100"
              min="0"
            />
          </td>
        </tr>
      </tbody>
    </table>
    <pick-user
      v-model="currentUsers"
      :show-invite-users="showInviteUsers"
      :text="inviteUsers"
      :users-ids="userIds"
    />
    <app-submit
      :running="running"
      class="green-btn"
      type="button"
      value="创建房间"
      @click.native="add"
    />
  </div>
</template>
<script lang="ts">
import {
  ApplyGrowlErr,
  State,
} from "@/ts/instances/storeInstance";
import {
  Component,
  Prop,
  Vue,
} from "vue-property-decorator";
import AppInputRange from "@/vue/ui/AppInputRange.vue";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import PickUser from "@/vue/parts/PickUser.vue";
import {
  ChannelsDictUIModel,
  CurrentUserInfoModel,
} from "@/ts/types/model";
import AppCheckbox from "@/vue/ui/AppCheckbox.vue";
import {PrivateRoomsIds} from "@/ts/types/types";

@Component({
  name: "CreateRoom",
  components: {
    AppCheckbox,
    AppInputRange,
    AppSubmit,
    PickUser,
  },
})
export default class CreateRoom extends Vue {
  @State
  public readonly privateRoomsUsersIds!: PrivateRoomsIds;

  @State
  public readonly userInfo!: CurrentUserInfoModel;

  @State
  public readonly channelsDictUI!: ChannelsDictUIModel;

  public currentUsers: number[] = [];

  public notifications: boolean = false;

  public sound: number = 0;

  public p2p: boolean = false;

  public roomName: string = "";

  public running: boolean = false;

  @Prop() public isPublic!: boolean;

  @Prop() public readonly parentChannelId!: number;

  @Prop()
  public readonly userIds!: number[];

  public get inviteUsers(): string {
    if (this.parentChannelId) {
      return `群组 ${this.channelsDictUI[this.parentChannelId].name} 中新房间的用户`;
    }
    return this.isPublic ? "邀请用户到新房间" : "选择私聊用户";
  }

  public get showInviteUsers() {
    return this.isPublic || this.currentUsers.length < 1;
  }


  @ApplyGrowlErr({runningProp: "running"})
  public async add() {
    if (this.isPublic && !this.roomName) {
      throw Error("请指定房间名称");
    }
    if (!this.isPublic && this.currentUsers.length === 0) {
      throw Error("请添加用户");
    }
    const e = await this.$ws.sendAddRoom(
      this.roomName ? this.roomName : null,
      this.isPublic ? false : this.p2p,
      this.sound,
      !this.p2p && this.notifications,
      this.currentUsers,
      this.parentChannelId ? this.parentChannelId : null,
    );
    this.$router.replace(`/chat/${e.roomId}`);
  }
}
</script>

<style lang="sass" scoped>
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
  max-width: 500px
  width: 100%

table
  width: 100%
  border-collapse: collapse
  margin-bottom: 24px

th, td
  padding: 12px 8px
  text-align: left
  border-bottom: 1px solid rgba(0, 0, 0, 0.05)

th
  font-weight: 600
  color: #374151
  width: 35%

input[type="text"]
  max-width: calc(100vw - 140px)
  border: 1px solid #d1d5db
  border-radius: 8px
  padding: 8px 12px
  font-size: 14px
  transition: all 0.2s ease
  
  &:focus
    outline: none
    border-color: #3b82f6
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1)

select
  width: 100%
  border: 1px solid #d1d5db
  border-radius: 8px
  padding: 8px 12px
  font-size: 14px
  transition: all 0.2s ease
  
  &:focus
    outline: none
    border-color: #3b82f6
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1)

.green-btn
  width: 100%
  flex-shrink: 0
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%)
  border: none
  border-radius: 12px
  padding: 16px 24px
  font-weight: 600
  font-size: 16px
  color: white
  transition: all 0.2s ease
  cursor: pointer
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2)
  
  &:hover
    transform: translateY(-2px)
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3)
  
  &:active
    transform: translateY(0)

// 美化复选框和滑块样式
:deep(.app-checkbox)
  display: flex
  align-items: center
  
  input[type="checkbox"]
    margin-right: 8px
    accent-color: #3b82f6

:deep(.app-input-range)
  width: 100%
  
  input[type="range"]
    width: 100%
    accent-color: #3b82f6

:deep(.pick-user)
  margin-bottom: 24px
  
  .pick-user-container
    border: 1px solid #e5e7eb
    border-radius: 8px
    padding: 16px
    background: rgba(248, 250, 252, 0.5)
</style>
