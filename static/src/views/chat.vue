<template>
  <div class="vw-100 vh-100">
    <div class="row m-0 p-0">
      <div class="col-2 p-0 z-index-25">
        <sideNav :userName="userName" :contactsList="contactsList" />
      </div>
      <div class="col-10 p-0">
        <chat-window
          :currentUserId="currentUserId"
          :rooms="rooms"
          :messages="messages"
          height="100vh"
          :theme="chatTheme"
          class="chat-widget-1"
        />
      </div>
    </div>
  </div>
</template>

<script>
const ChatWindow = () => import("vue-advanced-chat");
import "vue-advanced-chat/dist/vue-advanced-chat.css";
const sideNav = () => import("../components/sideNav.vue");

export default {
  name: "chat",
  components: {
    ChatWindow,
    sideNav,
  },
  mounted() {
    this.userName = localStorage.getItem("username") || "";
    this.getContacts();
  },
  data() {
    return {
      chatTheme: "light",
      userName: "",
      rooms: [],
      messages: [],
      currentUserId: 1,
      menuActions: "",
      messageActions: "",
      roomMessage: null,
      dataArray: [],
      contactsList: null,
    };
  },
  methods: {
    async getContacts() {
      try {
        const data = await this.$http.get("/dialogs");
        this.contactsList = data.data.dialogs;
      } catch (e) {
        console.log(e);
      }
    },
  },
};
</script>

<style scoped>
/deep/ .vac-rooms-container,
/deep/ .vac-room-header .vac-toggle-button {
  display: none !important;
}
</style>