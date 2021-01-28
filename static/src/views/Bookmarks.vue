<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='bookmarks-widget-1' :currentUserId='currentUserId' :messages='bookmarks'
          :single-room='true'
          :messages-loaded='false' @fetch-messages='loadOldMessages($event)' />
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
      currentUserId: 1,
      bookmarks: [],
      limit: 50,
      lastMessage: null,
    };
  },
  methods: {
    async fetchBookmarks() {
      try {
        const result = await MessageService.fetchFlaggedMessages();
        this.bookmarks = [{
          id: 2,
          room_id: 122955,
          message_id: 178,
          first_name: 'John Doe',
          message: 'Test',
          date: '2021-01-22T16:40:06.156602Z',
        }, ...result];
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>
<style scoped>
</style>
