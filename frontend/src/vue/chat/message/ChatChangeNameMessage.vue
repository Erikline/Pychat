<template>
  <chat-message-wrapper :time="time" class="message-system">
    <template #header>
      <span class="message-header"><span>系统</span>:</span>
    </template>
    <span class="message-text-style">
      此房间已被重命名，从 <b>{{ oldName }}</b> 到 <b>{{ newName }}</b>
    </span>
  </chat-message-wrapper>
</template>
<script lang="ts">
import {
  Component,
  Prop,
  Vue,
} from "vue-property-decorator";
import ChatMessageWrapper from "@/vue/chat/message/ChatMessageWrapper.vue";

@Component({
  name: "ChatChangeNameMessage",
  components: {ChatMessageWrapper},
})
export default class ChatChangeNameMessage extends Vue {
  @Prop() public time!: number;

  @Prop() public oldName!: string;

  @Prop() public newName!: string;
}
</script>

<style lang="sass" scoped>
.color-white .message-system
  background-color: #f2fbff
</style>
