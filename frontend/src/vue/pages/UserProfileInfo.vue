<template>
  <form
    class="holder"
    method="post"
    @submit.prevent="save"
  >
    <table>
      <tbody>
        <tr>
          <th>用户名:</th>
          <td>
            <input
              v-model="model.user"
              class="input"
              maxlength="30"
              type="text"
            />
          </td>
        </tr>
        <tr>
          <th>姓名:</th>
          <td>
            <input
              v-model="model.name"
              class="input"
              maxlength="30"
              type="text"
            />
          </td>
        </tr>
        <tr>
          <th>城市:</th>
          <td>
            <input
              v-model="model.city"
              class="input"
              maxlength="50"
              type="text"
            />
          </td>
        </tr>
        <tr>
          <th>姓氏:</th>
          <td>
            <input
              v-model="model.surname"
              class="input"
              maxlength="30"
              type="text"
            />
          </td>
        </tr>
        <tr>
          <th>生日:</th>
          <td>
            <app-input-date
              v-model="model.birthday"
              input-class="input"
              input-class-datepicker="input-date"
            />
          </td>
        </tr>
        <tr>
          <th>联系方式:</th>
          <td>
            <input
              v-model="model.contacts"
              class="input"
              maxlength="100"
              type="text"
            />
          </td>
        </tr>
        <tr>
          <th>性别:</th>
          <td>
            <select
              v-model="model.sex"
              class="input"
            >
              <option value="Male">男</option>
              <option value="Female">女</option>
              <option value="Secret">保密</option>
            </select>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <app-submit
              :running="running"
              class="green-btn"
              value="保存资料"
            />
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <app-submit
              class="red-btn"
              type="button"
              value="退出登录"
              @click.native="signOut"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </form>
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
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import type {SexModelString} from "@/ts/types/model";
import {CurrentUserInfoModel} from "@/ts/types/model";
import type {UserProfileDtoWoImage} from "@/ts/types/dto";

import {currentUserInfoModelToDto} from "@/ts/types/converters";
import AppInputDate from "@/vue/ui/AppInputDate.vue";
import type {SetUserProfileMessage} from "@/ts/types/messages/wsInMessages";
import type {LogoutMessage} from "@/ts/types/messages/innerMessages";

@Component({
  name: "UserProfileInfo",
  components: {
    AppInputDate,
    AppSubmit,
  },
})
export default class UserProfileInfo extends Vue {
  public running: boolean = false;

  @State
  public readonly userInfo!: CurrentUserInfoModel;

  public sex: SexModelString[] = ["Male", "Female", "Secret"];

  public model!: UserProfileDtoWoImage;

  public created() {
    this.model = currentUserInfoModelToDto(this.userInfo);
  }

  @ApplyGrowlErr({
    message: "保存资料时出错",
    runningProp: "running",
  })
  public async save() {
    this.$logger.debug("Saving userProfile")();
    const cui: UserProfileDtoWoImage = {...this.model};
    const e: SetUserProfileMessage | unknown = await this.$ws.saveUser(cui);
    this.$store.growlSuccess("用户资料已保存");
  }


  public async signOut() {
    this.$api.logout(); // Do not make user wait, logout instantly
    const message: LogoutMessage = {
      action: "logout",
      handler: "*",
    };
    this.$messageBus.notify(message);
  }
}
</script>

<style lang="sass" scoped>
.holder :deep(.input.input-date)
  width: 100%
</style>
