<template>
  <div class="top-div">
    <form
      v-if="channel"
      class="holder"
      @submit.prevent="apply"
    >
      <table>
        <tbody>
          <tr>
            <td colspan="2">
              群组 <b>{{ channel.name }}</b> 设置
            </td>
          </tr>
          <tr>
            <th>
              名称
            </th>
            <td>
              <input
                v-model="channelName"
                class="input"
                maxlength="16"
                required="true"
                type="text"
              />
            </td>
          </tr>
          <tr>
            <th>
              通知
            </th>
            <td>
              <app-checkbox v-model="notifications"/>
            </td>
          </tr>
          <tr>
            <th>
              声音
            </th>
            <td>
              <app-input-range
                v-model="sound"
                max="100"
                min="0"
              />
            </td>
          </tr>
          <tr>
            <th>管理员</th>
            <td v-if="isAdmin">
              <pick-user
                v-model="admin"
                :show-invite-users="showInviteUsers"
                :users-ids="userIds"
              />
            </td>
            <td v-else-if="currentAdmin">
              {{ currentAdmin.user }}
            </td>
            <!-- TODO remove fallback in future-->
            <td v-else>
              此频道没有管理员
            </td>
          </tr>
          <tr v-if="!isMain">
            <td colspan="2">
              <app-submit
              :running="running"
              class="red-btn"
              type="button"
              value="删除此群组"
              @click.native="deleteChannel"
            />
          </td>
        </tr>
        <tr v-if="!isMain">
          <td colspan="2">
            <app-submit
              :running="running"
              class="red-btn"
              type="button"
              value="离开此群组"
              @click.native="leaveChannel"
            />
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <app-submit
              :running="running"
              class="green-btn"
              value="应用设置"
            />
            </td>
          </tr>
        </tbody>
      </table>
    </form>
    <div v-else>
      频道 #{{ channelId }} 不存在
    </div>
  </div>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import type {
  ChannelUIModel,
  UserModel,
} from "@/ts/types/model";
import {
  ChannelsDictUIModel,
  CurrentUserInfoModel,
} from "@/ts/types/model";
import {
  ApplyGrowlErr,
  State,
} from "@/ts/instances/storeInstance";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import PickUser from "@/vue/parts/PickUser.vue";
import type {RouterNavigateMessage} from "@/ts/types/messages/innerMessages";
import {ALL_ROOM_ID} from "@/ts/utils/consts";
import AppInputRange from "@/vue/ui/AppInputRange.vue";
import AppCheckbox from "@/vue/ui/AppCheckbox.vue";

@Component({
  name: "ChannelSettings",
  components: {
    AppCheckbox,
    AppInputRange,
    PickUser,
    AppSubmit,
  },
})
export default class ChannelSettings extends Vue {
  public running: boolean = false;

  public channelName!: string;

  public admin: number[] = [];

  public sound: number = 0;

  public notifications: boolean = false;

  @State
  public readonly userInfo!: CurrentUserInfoModel;

  @State
  public readonly allUsersDict!: Record<number, UserModel>;

  @State
  public readonly channelsDictUI!: ChannelsDictUIModel;

  public get channel(): ChannelUIModel {
    return this.channelsDictUI[this.channelId];
  }

  public get showInviteUsers() {
    return this.admin.length < 1;
  }

  public get singleAdmin(): number {
    if (this.admin.length > 0) {
      return this.admin[0];
    }
    return this.channel.creator;
  }

  public get noRooms(): boolean {
    return this.channel.rooms.length === 0;
  }

  public get isAdmin(): boolean {
    return this.channel.creator === this.userInfo.userId;
  }

  public get isMain(): boolean {
    return this.channelId === ALL_ROOM_ID;
  }

  public get userIds(): number[] {
    return [...this.channel.mainRoom.users];
  }

  public get currentAdmin(): UserModel {
    return this.allUsersDict[this.channel.creator];
  }

  public get channelId(): number {
    const id = this.$route.params.id as string;
    this.$logger.log("Rending channel settings for {}", id)();

    return parseInt(id);
  }

  @ApplyGrowlErr({runningProp: "running"})
  async apply() {
    if (this.isAdmin && this.admin.length === 0) {
      throw Error("请选择一个管理员");
    }
    await this.$ws.saveChannelSettings(
      this.channelName,
      this.channelId,
      this.singleAdmin,
      this.sound,
      this.notifications,
    );
    this.$store.growlSuccess("设置已保存");
    this.$router.go(-1);
  }

  @ApplyGrowlErr({runningProp: "running"})
  public async leaveChannel(): Promise<void> {
    if (!confirm(`确定要离开群组 ${this.channel.name} 吗？`)) {
      return;
    }
    await this.$ws.sendLeaveChannel(this.channelId);
    this.goToMain();
    this.$store.growlSuccess("已离开频道");
    // 离开频道后自动刷新页面
    window.location.reload();
  }

  @ApplyGrowlErr({runningProp: "running"})
  public async deleteChannel(): Promise<void> {
    if (!confirm(`确定要删除群组 ${this.channel.name} 吗？`)) {
      return;
    }
    await this.$ws.sendDeleteChannel(this.channelId);
    this.goToMain();
    this.$store.growlSuccess("频道已删除");
    // 删除频道后自动刷新页面
    window.location.reload();
  }

  created() {
    this.$logger.log("Updated for channel settings {} ", this.channel)();
    this.channelName = this.channel.name;
    this.admin = [this.channel.creator];
    this.sound = this.channel.mainRoom.volume;
    this.notifications = this.channel.mainRoom.notifications;
  }

  private goToMain() { // TODO, should go back instead of main
    const message1: RouterNavigateMessage = {
      handler: "router",
      action: "navigate",
      to: `/chat/${ALL_ROOM_ID}`,
    };
    this.$messageBus.notify(message1);
  }
}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>

.top-div
  display: flex
  justify-content: center

.holder
  overflow-y: auto
  display: flex
  justify-content: center
  align-items: center

  input[type=text]
    width: 150px

  th
    text-align: right

  th, td
    padding: 5px

  td
    text-align: center

    > *
      margin: auto

    &[colspan="2"] > *
      width: 100%
</style>
