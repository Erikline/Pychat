<template>
  <div class="holder">
    <table>
      <tbody>
        <tr>
          <th>
            名称
          </th>
          <td>
            <input
              v-model="channelName"
              class="input"
              maxlength="16"
              type="text"
            />
          </td>
        </tr>
      </tbody>
    </table>
    <pick-user
      v-model="currentUsers"
      :users-ids="userIds"
      text="Invite users"
    />
    <app-submit
      :running="running"
      class="green-btn"
      type="button"
      value="创建群组"
      @click.native="add"
    />
  </div>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import {ALL_ROOM_ID} from "@/ts/utils/consts";
import {ApplyGrowlErr} from "@/ts/instances/storeInstance";
import PickUser from "@/vue/parts/PickUser.vue";

@Component({
  name: "CreateChannel",
  components: {
    PickUser,
    AppSubmit,
  },
})
export default class CreateChannel extends Vue {
  public channelName: string = "";

  public running: boolean = false;

  public currentUsers: number[] = [];


  public get userIds(): number[] {
    return this.$store.usersArray.map((u) => u.id);
  }

  @ApplyGrowlErr({
    runningProp: "running",
    message: "Unable to add channel",
  })
  public async add() {
    if (!this.channelName) {
      throw Error("Please specify a channel name");
    }
    const e = await this.$ws.sendAddChannel(this.channelName, this.currentUsers);
    this.$store.growlSuccess(`Channel '${this.channelName}' has been created`);
    this.$router.replace(`/chat/${ALL_ROOM_ID}`);
  }
}
</script>
<!-- eslint-disable -->
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
  width: 30%

input[type="text"]
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

// 美化用户选择组件
:deep(.pick-user)
  margin-bottom: 24px
  
  .pick-user-container
    border: 1px solid #e5e7eb
    border-radius: 8px
    padding: 16px
    background: rgba(248, 250, 252, 0.5)
</style>
