<template>
  <div class="settings-page modern-settings">
    <div class="settings-header">
      <span class="header-icon">⚙️</span> 个人设置
    </div>
    <table>
      <tbody>
        <tr>
          <th>输入建议:</th>
          <td>
            <app-checkbox v-model="model.suggestions"/>
          </td>
        </tr>
        <tr>
          <th>显示我正在输入消息</th>
          <td>
            <app-checkbox v-model="model.showWhenITyping"/>
          </td>
        </tr>

        <tr>
          <th>消息提示音:</th>
          <td>
              <app-checkbox v-model="model.messageSound"/>
          </td>
        </tr>
        <tr>
          <th>接收文件通话提示音:</th>
          <td>
            <app-checkbox v-model="model.incomingFileCallSound"/>
          </td>
        </tr>
        <tr>
          <th>在线状态变化提示:</th>
          <td>
            <app-checkbox v-model="model.onlineChangeSound"/>
          </td>
        </tr>
        <tr>
          <th>开发工具日志:</th>
          <td>
            <select v-model="model.logs" class="input">
              <option v-for="level in logLevels" :value="level">
                {{ level }}
              </option>
            </select>
          </td>
        </tr>
        <tr>
          <th>自动错误报告:</th>
          <td>
            <app-checkbox v-model="model.sendLogs"/>
          </td>
        </tr>
        <tr>
          <th>主题:</th>
          <td>
            <select
              v-model="model.theme"
              class="input"
              name="theme"
            >
              <option
                selected
                value="color-reg"
              >
                现代
              </option>
              <option value="color-lor">
                简约
              </option>
              <option value="color-white">
                浅色(测试版)
              </option>
            </select>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <input
              class="lor-btn"
              type="button"
              value="清除应用缓存"
              @click="clearHistory"
            />
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <input
              v-if="canBeInstalled"
              class="lor-btn"
              type="button"
              value="添加到主屏幕"
              @click="addToHomeScreen"
            />
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <app-submit
              :running="running"
              class="green-btn"
              value="应用设置"
              @click.native="save"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script lang="ts">
import {
  Component,
  Vue,
  Watch,
} from "vue-property-decorator";
import {
  ApplyGrowlErr,
  State,
} from "@/ts/instances/storeInstance";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import AppCheckbox from "@/vue/ui/AppCheckbox.vue";
import {CurrentUserSettingsModel} from "@/ts/types/model";
import {userSettingsDtoToModel} from "@/ts/types/converters";
import type {UserSettingsDto} from "@/ts/types/dto";
import type {SetSettingsMessage} from "@/ts/types/messages/wsInMessages";
import type {LogLevel} from "lines-logger";
import {logLevels} from "lines-logger";
import {
  LAST_SYNCED,
  SERVICE_WORKER_VERSION_LS_NAME,
} from "@/ts/utils/consts";
import {
  addToHomeScreen,
  canBeInstalled,
} from "@/ts/utils/addToHomeScreen";

@Component({
  name: "UserProfileSettings",
  components: {
    AppSubmit,
    AppCheckbox,
  },
})
export default class UserProfileSettings extends Vue {
  public running: boolean = false;

  public canBeInstalled: boolean = true;

  @State
  public readonly userSettings!: CurrentUserSettingsModel;

  public model!: UserSettingsDto;

  public readonly logLevels: LogLevel[] = Object.keys(logLevels) as LogLevel[];

  public async created() {
    this.model = userSettingsDtoToModel(this.userSettings);
    this.canBeInstalled = await canBeInstalled();
  }

  @Watch("userSettings", {deep: true})
  public onUserSettingsChange() {
    this.model = userSettingsDtoToModel(this.userSettings);
  }

  public async addToHomeScreen() {
    await addToHomeScreen();
  }

  public async clearHistory() {
    if (!confirm("This action will delete Service Worker cache and Websql data on your device. Proceed?")) {
      return;
    }

    /*
     * Do not remove lastSynced, instead set it to now
     * because if we go offline after clearing cache
     * message that are printing after it, won't appear while offline
     * to reproduce: chance to reproduce 50%.
     * Open 2 browsers (lets say chrome, + chrome annon).
     * Clear history on 2nd one. Type  `window.ws.ws.close()` on 2nd one.
     * Clicly switch to first one and send message in less than 5 seconds (reconnect time).
     * Open 2nd one and when internet appears the message might not appear while you were offline
     */
    localStorage.setItem(LAST_SYNCED, Date.now().toString());
    if (typeof self !== "undefined") {
      const cacheNames = await self.caches.keys();
      await Promise.all(cacheNames.map(async(cn) => {
        this.$logger.log(`Deleting cache '${cn}'`)();
        return caches.delete(cn);
      }));
    }
    localStorage.removeItem(SERVICE_WORKER_VERSION_LS_NAME);
    this.$store.clearMessages();
    this.$store.growlSuccess("Cash has been deleted ");
  }

  @ApplyGrowlErr({
    message: "Error saving settings",
    runningProp: "running",
  })
  public async save() {
    this.$logger.debug("Saving userSettings")();
    const cui: UserSettingsDto = {...this.model};
    const e: SetSettingsMessage | unknown = await this.$ws.saveSettings(cui);
    this.$store.growlSuccess("Settings have been saved");
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/partials/abstract_classes"

.modern-settings
  @extend %room-settings-holder
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)
  border-radius: 15px
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1)
  padding: 30px
  margin: 20px
  backdrop-filter: blur(10px)

.settings-header
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

.settings-page
  :deep(button)
    width: 100%
  padding-top: 10px
  padding-bottom: 10px

  :deep(table)
    margin: auto
    border-collapse: separate
    border-spacing: 0 15px
    width: 100%

  :deep(th)
    color: #fff !important
    font-weight: 500
    text-align: right
    padding: 15px 20px
    background: rgba(255, 255, 255, 0.1)
    border-radius: 10px 0 0 10px
    backdrop-filter: blur(5px)
    width: 40%

  :deep(td)
    padding: 15px 20px
    background: rgba(255, 255, 255, 0.05)
    border-radius: 0 10px 10px 0
    backdrop-filter: blur(5px)
    text-align: left

  :deep(.input)
    @extend %big-input
    background: rgba(255, 255, 255, 0.9)
    border: none
    border-radius: 8px
    padding: 12px 15px
    font-size: 16px
    transition: all 0.3s ease
    width: 100%
    max-width: 200px
    
    &:focus
      outline: none
      box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3)
      transform: translateY(-1px)

  :deep(.lor-btn)
    background: linear-gradient(135deg, #74b9ff, #0984e3)
    border: none
    border-radius: 10px
    padding: 12px 25px
    font-size: 16px
    font-weight: 600
    color: white
    cursor: pointer
    transition: all 0.3s ease
    box-shadow: 0 4px 15px rgba(9, 132, 227, 0.3)
    margin: 5px 0
    
    &:hover
      transform: translateY(-2px)
      box-shadow: 0 6px 20px rgba(9, 132, 227, 0.4)

  :deep(.green-btn)
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

  :deep(select)
    background: rgba(255, 255, 255, 0.9)
    border: none
    border-radius: 8px
    padding: 12px 15px
    font-size: 16px
    transition: all 0.3s ease
    cursor: pointer
    
    &:focus
      outline: none
      box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3)

  :deep(code)
    background: rgba(0, 0, 0, 0.2)
    padding: 2px 6px
    border-radius: 4px
    color: #fff
    font-family: 'Courier New', monospace

  :deep(b)
    color: #fff !important
    font-weight: 600

  :deep(div)
    color: rgba(255, 255, 255, 0.9) !important

  :deep(span)
    color: rgba(255, 255, 255, 0.9) !important
</style>
