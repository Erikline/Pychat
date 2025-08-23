<template>
  <div
    v-if="loading"
    class="spinner"
  />
  <div
    v-else-if="error"
    class="error"
  >
    {{ error }}
  </div>
  <div
    v-else-if="userProfileInfo"
    class="profileHolder"
  >
    <div v-if="userProfileInfo.image">
      <img :src="resolveMediaUrl(userProfileInfo.image)"/>
    </div>
    <div class="tableHolder">
      <table>
        <tbody>
          <tr>
            <th>用户名:</th>
            <td>{{ username }}</td>
          </tr>
          <tr>
            <th>姓名:</th>
            <td>{{ userProfileInfo.name }}</td>
          </tr>
          <tr>
            <th>城市:</th>
            <td>{{ userProfileInfo.city }}</td>
          </tr>
          <tr>
            <th>姓氏</th>
            <td>{{ userProfileInfo.surname }}</td>
          </tr>
          <tr>
            <th>邮箱:</th>
            <td>{{ userProfileInfo.email }}</td>
          </tr>
          <tr>
            <th>生日</th>
            <td>{{ userProfileInfo.birthday }}</td>
          </tr>
          <tr>
            <th>联系方式:</th>
            <td>{{ userProfileInfo.contacts }}</td>
          </tr>
          <tr>
            <th>性别:</th>
            <td>{{ userProfileInfo.sex }}</td>
          </tr>
        </tbody>
      </table>
    </div>
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
import {resolveMediaUrl} from "@/ts/utils/htmlApi";
import type {UserModel} from "@/ts/types/model";
import type {ViewUserProfileDto} from "@/ts/types/dto";

@Component({name: "ViewProfilePage"})
export default class ViewProfilePage extends Vue {
  public loading: boolean = false;

  public error: string | null = null;

  @State
  public readonly allUsersDict!: Record<number, UserModel>;

  public userProfileInfo: ViewUserProfileDto | null = null;

  public get id(): number {
    return parseInt(this.$route.params.id as string);
  }

  public get username(): string {
    const user = this.allUsersDict[this.id];
    return user ? user.user : "Unknown User";
  }

  public resolveMediaUrl(src: string) {
    return resolveMediaUrl(src);
  }

  @ApplyGrowlErr({
    vueProperty: "error",
    message: "加载用户信息时出错",
    runningProp: "loading",
  })
  public async created() {
    this.userProfileInfo = await this.$api.showProfile(this.id);
  }
}
</script>

<style lang="sass" scoped>

@import "@/assets/sass/partials/variables"
@import "@/assets/sass/partials/mixins"

th
  text-align: right

th, td
  padding: 0 5px

.error
  padding: 10px
  display: flex
  align-self: center
  font-size: 15px

.spinner
  @include lds-30-spinner-vertical('正在加载用户信息...')

.profileHolder
  display: flex
  flex-direction: row

  > div
    flex-grow: 1
    flex-basis: 0
    padding: 10px

.tableHolder
  display: flex
  justify-content: center

img
  width: 100%

@media screen and (max-width: $collapse-width)
  .profileHolder
    flex-direction: column

</style>
