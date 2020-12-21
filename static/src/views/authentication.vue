<template>
  <div class="auth">
    <div class="auth-container vw-100 vh-100 position-relative">
      <header>
        <div
          class="login-header width-404 position-absolute mx-auto left-right-0 d-grid justify-content-between align-items-center"
        >
          <div class="login-header-logo d-flex align-items-center">
            <i class="logo"></i>
            <h1 class="logo-text text-white d-flex align-items-center">
              mpact-Telegram
            </h1>
          </div>
          <div
            class="login-header-btn text-white cursor-pointer"
            :class="{ 'text-danger': !nextButtonValidation }"
            @click="nextButtonValidation && moveToNextPage()"
          >
            Next
            <i class="next-btn"></i>
          </div>
        </div>
      </header>
      <section class="position-relative">
        <div
          class="position-absolute mx-auto left-right-0 w-100 d-grid justify-content-center login-top"
        >
          <Login v-if="showLoginPage">
            <vue-tel-input
              v-model="phoneNumber"
              v-bind="telephoneProps"
              @validate="validatePhoneNumber($event)"
            ></vue-tel-input>
          </Login>
          <Otp
            v-if="showOtpPage"
            @hideOtpComponent="
              showOtpPage = !showOtpPage;
              showLoginPage = !showLoginPage;
            "
            @reciveOtpText="validateOTP($event)"
            :phone="phoneNumber"
          />
          <TwoFactorAuth
            v-if="show2FaPage"
            @recive2FaText="validate2FaText($event)"
          />
          <div class="login-footer width-404 text-center" v-show="!isInfoHide">
            <div class="footer-1">
              Welcome to the official mpact-Telegram web-client.
            </div>
            <div
              class="footer-2 cursor-pointer"
              @click="isInfoHide = !isInfoHide"
              v-show="!isInfoHide"
            >
              Learn more
            </div>
          </div>
          <Info
            v-if="isInfoHide"
            @closeInfoComponent="isInfoHide = false"
            v-bind:receiveClass="showOtpPage"
          />
        </div>
      </section>
      <Toast :text="toastInput" />
    </div>
  </div>
</template>
 <script>
const Login = () => import("../components/login.vue");
const Info = () => import("../components/telegramInfo.vue");
const Otp = () => import("../components/otp.vue");
const Toast = () => import("../components/toast.vue");
const TwoFactorAuth = () => import("../components/twoFactorAuth.vue");

import $ from "jquery";

export default {
  components: {
    Login,
    Info,
    Otp,
    Toast,
    TwoFactorAuth,
  },
  data() {
    return {
      isInfoHide: false,
      showOtpPage: false,
      showLoginPage: true,
      show2FaPage: false,
      nextButtonValidation: false,
      phoneNumber: "",
      toastInput: "",
      telephoneProps: {
        required: true,
        mode: "international",
      },
    };
  },
  methods: {
    async moveToNextPage() {
      if (this.showLoginPage) {
        console.log("submit phone number");

        this.showLoginPage = this.show2FaPage = false;
        this.showOtpPage = true;
      } else if (this.showOtpPage) {
        this.showOtpPage = this.showOtpPage = false;
        this.show2FaPage = true;
        console.log("submit otp");
        // const data = await this.$http.get(
        //   "https://jsonplaceholder.typicode.com/todos/1"
        // );
      } else {
        // this.$router.push('/chat');
      }
      $(".toast").toast("show");
      this.nextButtonValidation = false;
    },
    validatePhoneNumber(obj) {
      this.nextButtonValidation = obj.valid;
      this.toastInput = "OTP is sent to Registered Number";
    },
    validateOTP(obj) {
      this.nextButtonValidation = obj.toString().length >= 5;
      this.toastInput = "verifing the OTP";
    },
    validate2FaText(obj) {
      this.nextButtonValidation = obj.toString().length >= 5;
      this.toastInput = "verifing the 2FA code";
    },
  },
};
</script>
<style scoped>
header {
  height: 226px;
  background-color: var(--telegram-primary);
}

section {
  background-color: var(--telegram-secondary);
  height: calc(100vh - 226px);
}

.login-header {
  grid-template-columns: auto 78px;
  height: 75px;
  top: 95px;
}

.login-header-logo {
  padding: 23px 15px 22px;
  width: 140px;
  flex-direction: row;
}

.login-header-btn {
  justify-self: center;
  font-size: 13px;
  font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
  font-weight: 700;
  line-height: 20px;
}

.logo {
  width: 30px;
  height: 30px;
  display: inline-block;
  vertical-align: top;
  margin-right: 18px;
  background-image: url("../assets/telegram.png");
  background-repeat: no-repeat;
  background-position: -5px -10px;
  font-size: 13px;
  font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
}

.logo-text {
  width: 62px;
  height: 29px;
  display: inline-block;
  vertical-align: middle;
  background-repeat: no-repeat;
  background-position: 0 0;
  margin-top: 1px;
  white-space: nowrap;
  font-size: 14px;
  font: 13px/18px Tahoma, sans-serif, Arial, Helvetica;
}

.next-btn {
  width: 7px;
  height: 12px;
  display: inline-block;
  vertical-align: middle;
  margin-left: 12px;
  margin-top: -1px;
  background-image: url("../assets/telegram.png");
  background-repeat: no-repeat;
  background-position: -18px -50px;
}

.login-footer {
  color: #84a2bc;
  font-size: 13px;
  line-height: 16px;
  margin-top: 25px;
  top: 432px;
}

.login-top {
  top: -56px;
}
.footer-2 {
  color: var(--telegram-primary);
}
.footer-2:hover {
  text-decoration: underline;
}
.about-shown {
  margin-top: 25px;
}
.toast {
  top: 0;
  right: 0;
  left: 0;
  right: 0;
}
</style>