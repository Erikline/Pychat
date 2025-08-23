<template>
  <form
    id="register-form"
    ref="form"
    method="post"
    @submit.prevent="register"
  >
    <register-field-set
      icon="icon-user"
      :validation="userCheckValue"
      :closed="userFoc"
      :description="userDescription"
    >
      <input
        v-model.trim="username"
        v-validity="usernameValidity"
        type="text"
        maxlength="16"
        autocomplete="username"
        required
        placeholder="用户名"
        name="username"
        class="input"
        @focus="userFoc = false"
        @blur="userFoc = true"
      />
    </register-field-set>
    <register-field-set
      icon="icon-lock"
      :validation="passwordCheckValue"
      :closed="passwordFoc"
      :description="passwordDescription"
    >
      <input
        v-model="password"
        v-validity="passwordValidity"
        type="password"
        autocomplete="new-password"
        required
        name="password"
        class="input"
        placeholder="密码"
        @focus="passwordFoc = false"
        @blur="passwordFoc = true"
      />
    </register-field-set>
    <register-field-set
      icon="icon-lock"
      :validation="repPassCheckValue"
      :closed="repPassFoc"
      :description="repPassDescription"
    >
      <input
        v-model="repPass"
        v-validity="repPassValidity"
        autocomplete="new-password"
        type="password"
        required
        class="input"
        placeholder="重复密码"
        @focus="repPassFoc = false"
        @blur="repPassFoc = true"
      />
    </register-field-set>
    <register-field-set
      icon="icon-mail"
      :validation="emailCheckValue"
      :closed="emailFoc"
      :description="emailDescription"
    >
      <input
        v-model.trim="email"
        v-validity="emailValidity"
        type="email"
        autocomplete="email"
        placeholder="邮箱"
        name="email"
        class="input"
        @focus="emailFoc = false"
        @blur="emailFoc = true"
      />
    </register-field-set>
    <register-field-set i
      icon="icon-user-pair"
      :validation="sexCheckValue"
      :closed="sexFoc"
      :description="sexDescription"
    >
      <select
        v-model.trim="sex"
        name="sex"
        class="input"
        @focus="sexFoc = false"
        @blur="sexFoc = true"
      >
        <option
           value=""
           disabled
           selected
         >
           请选择性别
         </option>
        <option value="Male">
          男性
        </option>
        <option value="Female">
          女性
        </option>
      </select>
    </register-field-set>
    <app-submit
      class="submit-button"
      value="注册"
      :running="running"
    />
  </form>
</template>

<script lang='ts'>

import {
  Component,
  Prop,
  Ref,
  Vue,
  Watch,
} from "vue-property-decorator";
import {ApplyGrowlErr} from "@/ts/instances/storeInstance";
import AppSubmit from "@/vue/ui/AppSubmit.vue";
import RegisterFieldSet from "@/vue/singup/RegisterFieldSet.vue";
import debounce from "lodash.debounce";
import {IconColor} from "@/ts/types/types";
import {SexModelString} from "@/ts/types/model";
import type {LoginMessage} from "@/ts/types/messages/innerMessages";

import {USERNAME_REGEX} from "@/ts/utils/consts";

@Component({
  name: "SignUp",
  components: {
    AppSubmit,
    RegisterFieldSet},
})
export default class SignUp extends Vue {
  @Prop() public oauth_token!: string;

  @Prop() public fb_app_id!: string;


  running: boolean = false;

  @Ref()
  private form!: HTMLFormElement;

  created() {
    this.$store.setRegHeader("创建新账户");
    this.debouncedValidateUserName = debounce(this.checkUserName, 500);
    this.debouncedValidateEmail = debounce(this.checkEmail, 500);
  }


  userFoc: boolean = true;

  username: string = "";

  usernameValidity: string = "";

  passwordValidity: string = "";

  repPassValidity: string = "";

  emailValidity: string = "";

  userDescription: string = "请选择用户名";

  userCheckValue: IconColor = IconColor.NOT_SET;

  debouncedValidateUserName!: Function;


  private currentValidateUsernameRequest: XMLHttpRequest | null = null;

  async checkUserName(username: string) {
    if (this.currentValidateUsernameRequest) {
      this.currentValidateUsernameRequest.abort();
      this.currentValidateUsernameRequest = null;
    }
    try {
      await this.$api.validateUsername(username, (r) => this.currentValidateUsernameRequest = r);
      this.userCheckValue = IconColor.SUCCESS;
      this.userDescription = "用户名可用！";
      this.usernameValidity = "";
    } catch (errors: any) {
      this.userCheckValue = IconColor.ERROR;
      this.usernameValidity = errors;
      this.userDescription = errors;
    } finally {
      this.currentValidateUsernameRequest = null;
    }
  }

  @Watch("username")
  onUsernameChanged(username: string) {
    if (username === "") {
      this.userCheckValue = IconColor.ERROR;
      this.userDescription = "用户名不能为空";
      this.usernameValidity = this.userDescription;
    } else if (!new RegExp(USERNAME_REGEX).test(username)) {
      this.userDescription = "用户名只能包含拉丁字母、数字、破折号或下划线";
      this.usernameValidity = this.userDescription;
      this.userCheckValue = IconColor.ERROR;
    } else {
      this.usernameValidity = "检查中...";
      this.userCheckValue = IconColor.NOT_SET;
      this.debouncedValidateUserName(username);
    }
  }

  passwordFoc: boolean = true;

  password: string = "";

  passwordDescription: string = "密码至少8个字符";

  passwordCheckValue: IconColor = IconColor.NOT_SET;

  @Watch("password")
  onPasswordChange(pswd: string) {
    if (pswd.length === 0) {
      this.passwordDescription = "密码不能为空";
      this.passwordValidity = this.passwordDescription;
      this.passwordCheckValue = IconColor.ERROR;
    } else if (!(/^\S.+\S$/).test(pswd)) {
      this.passwordCheckValue = IconColor.ERROR;
      this.passwordDescription = "密码太短";
      this.passwordValidity = this.passwordDescription;
    } else if (!(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,}$/).test(pswd) && pswd.length < 11) {
      this.passwordDescription = "密码强度：弱";
      this.passwordValidity = "";
      this.passwordCheckValue = IconColor.WARN;
    } else if (pswd.length < 11) {
      this.passwordDescription = "密码强度：中";
      this.passwordValidity = "";
      this.passwordCheckValue = IconColor.SUCCESS;
    } else {
      this.passwordDescription = "密码强度：强";
      this.passwordValidity = "";
      this.passwordCheckValue = IconColor.SUCCESS;
    }
  }

  repPassFoc: boolean = true;

  repPass: string = "";

  repPassDescription: string = "重复密码";

  repPassCheckValue: IconColor = IconColor.NOT_SET;

  public get passRepPass() {
    return `${this.repPass}|${this.password}`;
  }

  @Watch("passRepPass")
  onRepPassChange(pswd: string) {
    if (this.repPass != this.password) {
      this.repPassCheckValue = IconColor.ERROR;
      this.repPassDescription = "密码不匹配";
      this.repPassValidity = this.repPassDescription;
    } else {
      this.repPassCheckValue = IconColor.SUCCESS;
      this.repPassValidity = "";
      this.repPassDescription = "密码匹配";
    }
  }

  emailFoc: boolean = true;

  email: string = "";

  emailDescription: string = "邮箱用于找回密码";

  emailCheckValue: IconColor = IconColor.NOT_SET;

  debouncedValidateEmail!: Function;

  private currentValidateEmailRequest: XMLHttpRequest | null = null;

  async checkEmail(username: string) {
    if (this.currentValidateEmailRequest) {
      this.currentValidateEmailRequest.abort();
      this.currentValidateEmailRequest = null;
    }
    try {
      await this.$api.validateEmail(username, (r) => this.currentValidateEmailRequest = r);
      this.emailCheckValue = IconColor.SUCCESS;
      this.emailDescription = "邮箱有效";
      this.emailValidity = "";
    } catch (errors: any) {
      this.emailCheckValue = IconColor.ERROR;
      this.emailValidity = errors;
      this.emailDescription = errors;
    } finally {
      this.currentValidateEmailRequest = null;
    }
  }


  destroyed(): void {
    if (this.currentValidateEmailRequest) {
      this.currentValidateEmailRequest.abort();
      this.currentValidateEmailRequest = null;
    }
    if (this.currentValidateUsernameRequest) {
      this.currentValidateUsernameRequest.abort();
      this.currentValidateUsernameRequest = null;
    }
  }


  @Watch("email")
  onEmailChange(email: string) {
    if (email === "") {
      this.emailCheckValue = IconColor.WARN;
      this.emailValidity = "";
      this.userDescription = "可以留空...";
    } else {
      this.emailCheckValue = IconColor.NOT_SET;
      this.emailValidity = "检查中...";
       this.debouncedValidateEmail(email);
     }
   }


   sexFoc: boolean = true;

   sex: string = "";

   sexDescription: string = "选择性别";

   sexCheckValue: IconColor = IconColor.NOT_SET;

   @Watch("sex")
   onSexChange(gender: string) {
     if (!gender) {
       this.sexCheckValue = IconColor.NOT_SET;
       this.sexDescription = "点击选择性别";
     } else if (gender === "Secret") {
       this.sexDescription = "需要帮助？";
       this.sexCheckValue = IconColor.WARN;
     } else {
       this.sexCheckValue = IconColor.SUCCESS;
       this.sexDescription = "性别已选择";
     }
   }

   @ApplyGrowlErr({runningProp: "running",
     message: "无法注册"})
   async register() {
     const {session} = await this.$api.register(this.form);
     const message: LoginMessage = {action: "login",
                                    handler: "router",
                                    session};
     this.$messageBus.notify(message);
   }
 }
</script>
