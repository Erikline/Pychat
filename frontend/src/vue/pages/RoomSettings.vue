<template>
  <form
    v-if="room"
    class="holder"
    @submit.prevent="apply"
  >
    <table>
      <tbody>
        <tr>
          <td v-if="room.name" class="room-heder" colspan="2">
            房间 <b>{{ room.name }}</b> 设置
          </td>
          <td v-else class="room-heder" colspan="2">
            用户 <b>{{ user }}</b> 设置
          </td>
        </tr>
        <tr v-if="isPublic">
          <th>
            Name
          </th>
          <td>
            <input
              v-model="roomName"
              :disabled="isMainRoom"
              :required="isPublic"
              class="input"
              maxlength="16"
              type="text"
            />
            <div v-if="!isPublic && roomName">
              为房间添加名称后，将使其变为公开房间
            </div>
          </td>
        </tr>
        <tr v-if="isPublic && !isMainRoom">
          <th>Admin</th>
          <td v-if="canChangeAdmin">
            <pick-user
              v-model="admin"
              :show-invite-users="showInviteUsers"
              :users-ids="userIds"
            />
          </td>
          <td v-else-if="oldAdmin">
            {{ oldAdmin.user }}
          </td>
          <td v-else>
            此房间没有管理员
          </td>
        </tr>
        <tr>
          <th>
            Notifications
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
        <tr v-if="!isPublic">
          <th>
            Peer to peer
          </th>
          <td>
            <app-checkbox v-model="p2p"/>
          </td>
        </tr>
        <tr v-if="!isMainRoom">
          <td colspan="2">
            <app-submit
              :running="running"
              class="red-btn"
              type="button"
              value="离开此房间"
              @click.native="leaveRoom"
            />
          </td>
        </tr>
        <tr v-if="isAdmin">
          <td colspan="2">
            <app-submit
              :running="running"
              class="red-btn"
              type="button"
              value="删除此房间"
              @click.native="deleteRoom"
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
    房间 #{{ roomId }} 不存在
  </div>
</template>
<script lang="ts">
import {
  ApplyGrowlErr,
  State,
} from "@/ts/instances/storeInstance";
import {
  Component,
  Vue,
} from "vue-property-decorator";
import AppInputRange from "@/vue/ui/AppInputRange.vue";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import AppCheckbox from "@/vue/ui/AppCheckbox.vue";
import type {
  RoomModel,
  UserModel,
} from "@/ts/types/model";
import {
  RoomDictModel,
  UserDictModel,
} from "@/ts/types/model";
import {ALL_ROOM_ID} from "@/ts/utils/consts";
import PickUser from "@/vue/parts/PickUser.vue";
import {PrivateRoomsIds} from "@/ts/types/types";


@Component({
  name: "RoomSettings",
  components: {
    PickUser,
    AppInputRange,
    AppSubmit,
    AppCheckbox,
  },
})
export default class RoomSettings extends Vue {
  public admin: number[] = [];

  public roomName: string = "";

  public sound: number = 0;

  public channelId: number | null = null;

  public notifications: boolean = false;

  public running: boolean = false;

  public isPublic: boolean = false;

  public p2p: boolean = false;

  @State
  public readonly myId!: number;

  @State
  public readonly roomsDict!: RoomDictModel;

  @State
  public readonly privateRoomsUsersIds!: PrivateRoomsIds;

  @State
  public readonly allUsersDict!: UserDictModel;

  public get room(): RoomModel {
    return this.roomsDict[this.roomId];
  }

  public get roomId(): number {
    const id = this.$route.params.id as string;
    this.$logger.log("Rending room settings for {}", id)();

    return parseInt(id);
  }

  public get user(): string | null {
    if (this.room.name) {
      return null;
    }
    const uId = this.privateRoomsUsersIds.roomUsers[this.room.id];
    const user = this.allUsersDict[uId];
    return user ? user.user : null;
  }

  public get isAdmin(): boolean {
    return this.room.creator === this.myId;
  }

  public get showInviteUsers() {
    return this.admin.length < 1;
  }

  public get canChangeAdmin() {
    return this.isPublic && (!this.room.creator || this.myId === this.room.creator);
  }

  public get userIds(): number[] {
    return [...this.room.users];
  }

  public get oldAdmin(): UserModel | null {
    if (this.room.creator) {
      return this.allUsersDict[this.room.creator];
    }
    return null;
  }

  public get isMainRoom(): boolean {
    return this.roomId === ALL_ROOM_ID;
  }

  public get singleAdmin(): number {
    if (this.admin.length > 0) {
      return this.admin[0];
    }
    return this.room.creator;
  }

  public created() {
    this.setVars();
  }

  @ApplyGrowlErr({runningProp: "running"})
  public async deleteRoom() {
    if (this.room.name && !confirm(`Are you sure you want to delete room ${this.room.name}`)) {
      return;
    }
    this.$logger.log("deleting room {}", this.roomId)();
    await this.$ws.sendDeleteRoom(this.roomId);
  }

  @ApplyGrowlErr({runningProp: "running"})
  public async leaveRoom() {
    if (this.room.name && !confirm(`Are you sure you want to leave room ${this.room.name}`)) {
      return;
    }
    this.$logger.log("Leaving room {}", this.roomId)();
    await this.$ws.sendLeaveRoom(this.roomId);
  }

  @ApplyGrowlErr({
    runningProp: "running",
    message: "Can't set room settings",
  })
  public async apply() {
    this.$logger.log("Applying room {} settings", this.roomId)();
    await this.$ws.sendRoomSettings({
      roomCreatorId: this.singleAdmin,
      volume: this.sound,
      notifications: this.notifications,
      name: this.roomName,
      isMainInChannel: this.room.isMainInChannel,
      roomId: this.roomId,
      p2p: this.p2p,
      channelId: this.channelId,
    });
    this.$store.growlSuccess("Settings has been saved");
    this.$router.replace(`/chat/${this.roomId}`);
  }

  private setVars() {
    this.$logger.log("Updated for room settings {} ", this.room)();
    if (this.room) {
      this.roomName = this.room.name;
      this.isPublic = Boolean(this.roomName);
      this.sound = this.room.volume;
      this.notifications = this.room.notifications;
      this.p2p = this.room.p2p;
      this.channelId = this.room.channelId;
      if (this.room.creator) {
        this.admin = [this.room.creator];
      } else {
        this.admin = [];
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/partials/abstract_classes"

.modern-card
  @extend %room-settings-holder
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
  border-radius: 15px
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1)
  padding: 30px
  margin: 20px
  backdrop-filter: blur(10px)

.holder
  @extend %room-settings-holder
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
  border-radius: 15px
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1)
  padding: 30px
  margin: 20px
  backdrop-filter: blur(10px)
  overflow-y: auto
  height: 100%
  display: flex
  align-items: center

.room-heder
  font-size: 24px
  font-weight: 600
  color: #fff
  text-align: center
  padding-bottom: 25px
  border-bottom: 1px solid rgba(255, 255, 255, 0.2)
  margin-bottom: 20px

.header-icon
  font-size: 28px
  margin-right: 10px
  vertical-align: middle

table
  width: 100%
  border-collapse: separate
  border-spacing: 0 15px

th
  color: #fff !important
  font-weight: 500
  text-align: right
  padding: 15px 20px
  background: rgba(255, 255, 255, 0.1)
  border-radius: 10px 0 0 10px
  backdrop-filter: blur(5px)
  width: 40%

td
  padding: 15px 20px
  background: rgba(255, 255, 255, 0.05)
  border-radius: 0 10px 10px 0
  backdrop-filter: blur(5px)
  text-align: left

  > *
    margin: 0

input[type=text]
  width: 100%
  max-width: 200px
  background: rgba(255, 255, 255, 0.9)
  border: none
  border-radius: 8px
  padding: 12px 15px
  font-size: 16px
  transition: all 0.3s ease

  &:focus
    outline: none
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3)
    transform: translateY(-1px)

.red-btn
  background: linear-gradient(135deg, #ff6b6b, #ee5a24)
  border: none
  border-radius: 10px
  padding: 12px 25px
  font-size: 16px
  font-weight: 600
  color: white
  cursor: pointer
  transition: all 0.3s ease
  box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3)
  width: 100%

  &:hover
    transform: translateY(-2px)
    box-shadow: 0 6px 20px rgba(238, 90, 36, 0.4)

.green-btn
  background: linear-gradient(135deg, #51cf66, #40c057)
  border: none
  border-radius: 10px
  padding: 12px 25px
  font-size: 16px
  font-weight: 600
  color: white
  cursor: pointer
  transition: all 0.3s ease
  box-shadow: 0 4px 15px rgba(64, 192, 87, 0.3)
  width: 100%

  &:hover
    transform: translateY(-2px)
    box-shadow: 0 6px 20px rgba(64, 192, 87, 0.4)

b
  color: #fff !important
  font-weight: 600

div
  color: rgba(255, 255, 255, 0.9) !important

span
  color: rgba(255, 255, 255, 0.9) !important
</style>
