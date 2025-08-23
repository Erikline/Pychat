<template>
  <div class="oauth-div">
    <app-submit
      v-if="facebookConnected"
      class="red-btn"
      value="Disconnect Facebook account"
      @click.native="disconnectFacebook"
    />
    <div v-else class="oauth-placeholder">Facebook authentication is not available</div>

    <app-submit
      v-if="googleConnected"
      class="red-btn"
      value="Disconnect Google account"
      @click.native="disconnectGoogle"
    />
    <div v-else class="oauth-placeholder">Google authentication is not available</div>
  </div>
</template>
<script lang="ts">
import {
  Component,
  Vue,
} from "vue-property-decorator";
import type {OauthStatus} from "@/ts/types/dto";
import AppSubmit from "@/vue/ui/AppSubmit.vue";

@Component({
  name: "UserProfileOauthSettings",
  components: {
    AppSubmit,
  },
})
export default class UserProfileOauthSettings extends Vue {
  public googleConnected: boolean = false;

  public facebookConnected: boolean = false;


  async created() {
    const response: OauthStatus = await this.$api.getOauthStatus();
    this.googleConnected = response.google;
    this.facebookConnected = response.facebook;
  }

  async disconnectGoogle() {
    await this.$api.setGoogleOauth("");
    this.googleConnected = false;
    this.$store.growlSuccess("Google account has been disconnected");
  }

  async disconnectFacebook() {
    await this.$api.setFacebookOauth("");
    this.facebookConnected = false;
    this.$store.growlSuccess("Facebook account has been disconnected");
  }

  // OAuth authentication methods removed as components are not available
}
</script>

<style lang="sass" scoped>
.oauth-div
  margin: auto
  max-width: 500px
  text-align: center

  > *
    display: inline-block
    margin: 10px
    width: 220px !important

.oauth-placeholder
  padding: 10px
  color: #666
  font-style: italic
  border: 1px dashed #ccc
  border-radius: 4px
  background-color: #f9f9f9
</style>
