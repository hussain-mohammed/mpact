<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='bookmarks-widget-1' :currentUserId='currentUserId' :messages='bookmarks'
          :single-room='true' :rooms-loaded='true' :rooms='rooms' :text-messages="textMessages"
          :show-footer='false' :show-emojis='false' :show-reaction-emojis='false' :messages-loaded='bookmarksLoaded'
          @fetch-messages='fetchMoreBookmarks($event)' :message-actions='messageActions'
          :styles='styles' :show-new-messages-divider='false'
          @message-action-handler='messageActionHandler($event)'/>
      </div>
    </div>
  </div>
</template>
<script>
import MessageService from '../services/MessageService';
import { convertDate, convertTime } from '../utils/helpers';
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
      rooms: [],
      messages: [],
      limit: 50,
      offset: 0,
      lastMessage: null,
      bookmarksLoaded: false,
      messageActions: [
        {
          name: 'unFlagMessage',
          title: 'Remove Flag',
        },
      ],
      textMessages: {
        ROOMS_EMPTY: 'No flagged messages to show',
        ROOM_EMPTY: 'No flagged messages to show',
        MESSAGES_EMPTY: 'No flagged messages to show',
        CONVERSATION_STARTED: '',
      },
      styles: {
      },
    };
  },
  mounted() {
    try {
      this.fetchBookmarks();
    } catch (err) {
      console.error(err);
    }
  },
  methods: {
    async messageActionHandler({ roomId, action, message }) {
      try {
        const options = { roomId, message };
        switch (action.name) {
        case 'unFlagMessage':
          this.unFlagMessage(options);
          break;
        default:
          break;
        }
      } catch (err) {
        console.error(err);
      }
    },
    async fetchBookmarks() {
      try {
        const result = await MessageService.fetchFlaggedMessages({});
        if (result && result.data.flagged_messages) {
          this.currentUserId = 1512271983;
          const formattedMessages = [];
          result.data.flagged_messages.forEach((d) => {
            formattedMessages.push({
              _id: d.id,
              content: d.message || '',
              sender_id: d.sender || 1,
              date: convertDate(d.date),
              timestamp: convertTime(d.date),
            });
          });
          this.bookmarks = formattedMessages;
          this.rooms = [{
            roomId: 1,
            roomName: 'Bookmarks',
            users: [],
          }];
          if (formattedMessages.length < 50) {
            this.bookmarksLoaded = true;
          }
        }
      } catch (err) {
        console.error(err);
      }
    },
    async fetchMoreBookmarks({
      options = {},
    }) {
      try {
        const {
          reset = false,
        } = options;
        if (reset) {
          return;
        }
        const params = {
          offset: this.offset,
          limit: this.limit,
        };
        const result = await MessageService.fetchFlaggedMessages(params);
        if (result && result.data.flagged_messages) {
          const formattedMessages = [];
          result.data.flagged_messages.forEach((d) => {
            formattedMessages.push({
              _id: d.id,
              content: d.message || '',
              sender_id: d.sender || 1,
              date: convertDate(d.date),
              timestamp: convertTime(d.date),
            });
          });
          this.bookmarks = [formattedMessages, ...this.bookmarks];
          this.rooms = [{
            roomId: 1,
            roomName: 'Bookmarks',
            users: [],
          }];
          if (formattedMessages.length < 50) {
            this.bookmarksLoaded = true;
          }
        }
      } catch (err) {
        console.error(err);
      }
    },
    async unFlagMessage({ message }) {
      try {
        const id = message._id;
        const params = {
          id,
        };
        const response = await MessageService.unFlagMessage(params);
        if (response && response.data.is_success) {
          const updatedBookmarks = this.bookmarks.filter((bookmark) => bookmark._id !== id);
          this.bookmarks = updatedBookmarks;
        }
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>
<style scoped>
.row {
  justify-content: center;
}
</style>
