<template>
  <div class="callContainerIcons">
    <div v-if="callInfo.callActiveButNotJoinedYet" class="call-is-active">
      此房间的通话已激活
    </div>
    <div class="callContainerIconsInner">
      <button v-if="callInfo.callActiveButNotJoinedYet" class="green-btn" @click="joinCall">
        加入通话
      </button>
      <i
        :class="iconMicClass"
        :title="micTitle"
        @click="micClick"
      />
      <i
        :class="iconVideoClass"
        :title="videoTitle"
        @click="videoClick"
      />
      <i
        :class="callInfo.shareScreen ? 'activeIcon' : 'noactiveIcon'"
        class="icon-desktop"
        title="捕获桌面屏幕并开始共享"
        @click="desktopClick"
      />
      <i
        :class="callInfo.sharePaint ? 'activeIcon' : 'noactiveIcon'"
        class="icon-brush"
        title="共享画板"
        @click="paintClick"
      />
      <i
        v-show="callInfo.callActive"
        class="icon-popup"
        title="隐藏/显示视频"
        @click="invertShowVideoContainer"
      />
      <i
        class="icon-cog"
        @click="invertShowSettings"
      />
      <i
        v-show="callInfo.callActive"
        class="icon-webrtc-fullscreen"
        title="全屏显示"
        @click="enterFullscreen"
      />
      <div
        v-show="callInfo.callActive"
        class="hangUpHolder"
      >
        <i
          class="icon-hang-up"
          title="挂断通话"
          @click="hangUpCall"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Emit,
  Prop,
  Vue,
} from "vue-property-decorator";
import {CallsInfoModel} from "@/ts/types/model";

@Component({name: "CallContainerIcons"})
export default class CallContainerIcons extends Vue {
  @Prop() public callInfo!: CallsInfoModel;

  @Prop() public roomId!: number;

  public get videoTitle() {
    return `${this.callInfo.showVideo ? "关闭" : "打开"}摄像头`;
  }

  public get micTitle() {
    return `${this.callInfo.showMic ? "关闭" : "打开"}麦克风`;
  }

  public get iconVideoClass(): {} {
    return {
      "icon-no-videocam": !this.callInfo.showVideo,
      "icon-videocam": this.callInfo.showVideo,
    };
  }

  public get iconMicClass(): {} {
    return {
      "icon-mic": this.callInfo.showMic,
      "icon-mute": !this.callInfo.showMic,
    };
  }

  @Emit()
  public micClick(): void {
  }

  @Emit()
  public hangUpCall(): void {
  }

  @Emit()
  public videoClick(): void {
  }

  @Emit()
  public desktopClick(): void {
  }

  @Emit()
  public invertShowSettings(): void {
  }

  @Emit()
  public enterFullscreen(): void {
  }

  @Emit()
  public paintClick(): void {
  }

  @Emit()
  public invertShowVideoContainer(): void {
  }

  public joinCall(): void {
    this.$webrtcApi.joinCall(this.roomId);
  }
}
</script>
<!-- eslint-disable -->
<style lang="sass" scoped>
@import "@/assets/sass/partials/mixins"

.call-is-active
  font-size: 10px

.icon-webrtc-fullscreen
  padding-top: 1px
  margin-bottom: -1px
  transform: scale(2)

.callContainerIcons
  display: flex
  flex-direction: column
  font-size: 25px
  @extend %user-select-none
  width: 100%
  padding-top: 10px

  .callContainerIconsInner
    display: flex
    margin: auto
    justify-content: space-between

    > *
      margin: 0 5px

  .hangUpHolder
    display: inline-block
    position: relative
    width: 46px
    height: 28px
    margin-left: 10px
    margin-top: -7px

    .icon-hang-up
      position: absolute
      font-size: 35px
      top: 0
      left: 0

</style>
