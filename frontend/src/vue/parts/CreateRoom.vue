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

input[type="text"]
  max-width: calc(100vw - 140px)

.holder
  @extend %room-settings-holder

select
  width: 100%

th, td
  padding: 5px

.green-btn
  width: 100%
  flex-shrink: 0

</style>
