<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='bookmarks-widget-1' :currentUserId='currentUserId'
        :messages='bookmarks' :messages-loaded='fetchBookmarks'
        @fetch-messages='loadOldMessages($event)' />
      </div>
    </div>
  </div>
</template>
<script>
import MessageService from '../services/MessageService';
import 'vue-advanced-chat/dist/vue-advanced-chat.css';

const ChatWindow = () => import('vue-advanced-chat');
export default {
  name: 'bookmarks',
  components: {
    ChatWindow,
  },
  data() {
    return {
      currentUserId: '',
      bookmarks: [],
    };
  },
  methods: {
    async fetchBookmarks() {
      try {
        const result = await MessageService.fetchFlaggedMessages();
        this.bookmarks = result;
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>
<style scoped>
</style>
