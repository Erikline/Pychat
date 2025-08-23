<template>
  <app-modal>
    <div class="app-menu-bar">
      <div class="app-header">
        <span class="username">
          <img v-if="imgSrc" :src="imgSrc"/>
          <div class="user-name">{{ userInfo.user }}</div>
        </span>
      </div>
      <div class="app-section">
        <router-link
          title="创建新的私聊房间"
          to="/create-private-room"
        >
          私聊用户
        </router-link>
        <router-link
          title="创建新的群组房间"
          to="/create-group"
        >
          创建群组
        </router-link>
        <router-link title="个人设置" to="/profile">
          个人资料
        </router-link>
        <router-link to="/settings">
          设置
        </router-link>
        <router-link
          v-if="consts.ISSUES"
          title="提交问题反馈"
          to="/report-issue"
        >
          问题反馈
        </router-link>

        <a
          href="#"
          title="退出登录"
          @click.prevent="signOut"
        >
          退出登录
        </a>
      </div>
    </div>
  </app-modal>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import {
  ISSUES,
} from "@/ts/utils/consts";
import {State} from "@/ts/instances/storeInstance";
import {CurrentUserInfoModel} from "@/ts/types/model";
import AppModal from "@/vue/ui/AppModal.vue";
import {resolveMediaUrl} from "@/ts/utils/htmlApi";

@Component({
  name: "AppMenuBar",
  components: {
    AppModal,
  },
})
export default class AppMenuBar extends Vue {
  @State
  public readonly userInfo!: CurrentUserInfoModel;

  public get imgSrc() {
    return resolveMediaUrl(this.userInfo.image);
  }

  public get consts() {
    return {
      ISSUES,
    };
  }

  public signOut() {
    this.$api.logout(); // 立即退出登录，不等待响应
    const message = {
      action: "logout",
      handler: "*" as const,
    };
    this.$messageBus.notify(message);
    this.$emit("click"); // 关闭菜单
  }
}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>

.app-menu-bar
  font-size: 25px
  background-color: #f8fafc
  border: 1px #d1d5db solid
  width: 200px

.user-name
  font-size: 17px
  font-weight: bold
  margin-top: 5px

img
  border-radius: 50%
  width: 100px
  max-height: 120px

%app-common
  padding: 10px

.app-header
  background-color: #e2e8f0
  padding: 10px 15px 5px
  @extend %app-common

.app-section
  @extend %app-common
  display: flex
  flex-direction: column

  > *
    padding: 5px

    &:hover
      color: #f0f0f0

</style>
