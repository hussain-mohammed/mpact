<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='bookmarks-widget-1' :currentUserId='currentUserId' :messages='bookmarks'
          :single-room='true' :rooms-loaded='true' :rooms='rooms' :text-messages="textMessages"
          :show-footer='false' :messages-loaded='bookmarksLoaded' @fetch-messages='fetchMoreBookmarks($event)'
          :message-actions='messageActions' @message-action-handler='messageActionHandler($event)'/>
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
        ROOMS_EMPTY: 'No flagged message to show',
        ROOM_EMPTY: 'No flagged message to show',
        MESSAGES_EMPTY: 'No flagged message to show',
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
        this.currentUserId = 1512271983;
        const formattedMessages = [];
        result.data.flagged_message.forEach((d) => {
          formattedMessages.push({
            _id: d.id,
            content: d.message,
            sender_id: d.sender || '',
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
        this.bookmarksLoaded = true;
      } catch (err) {
        console.error(err);
      }
    },
    async fetchMoreBookmarks() {
      try {
        const params = {
          offset: this.offset,
          limit: this.limit,
        };
        await MessageService.fetchFlaggedMessages(params);
      } catch (err) {
        console.error(err);
      }
    },
    async unFlagMessage({ message }) {
      try {
        const params = {
          id: message._id,
        };
        await MessageService.deleteFlaggedMessage(params);
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>
<style scoped>
</style>
