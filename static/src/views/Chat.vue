<template>
  <div class='vw-100 vh-100'>
    <div class='row m-0 p-0'>
      <div class='col-2 p-0 z-index__25'>
        <side-nav :userName='userName' :contactsList='contactsList'
          @getIndividualMessages='getIndividualMessages($event)'
          @getGroupMessages='getGroupMessages($event)' />
      </div>
      <div class='col-10 p-0'>
        <chat-window height='100vh' class='chat-widget-1' :currentUserId='currentUserId'
        :rooms='rooms' :messages='messages' :single-room='hideSideNav'
         :messages-loaded='messagesLoaded' @fetch-messages='loadOldMessages($event)'
         @send-message='sendMessage($event)' :message-actions='messageActions'
         @message-action-handler='messageActionHandler($event)'/>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable import/no-named-as-default-member */
import MessageService from '../services/MessageService';
import dateHelpers from '../utils/helpers/dateHelpers';
import 'vue-advanced-chat/dist/vue-advanced-chat.css';

const ChatWindow = () => import('vue-advanced-chat');
const SideNav = () => import('../components/SideNav.vue');

export default {
  name: 'chat',
  components: {
    ChatWindow,
    SideNav,
  },
  mounted() {
    this.userName = localStorage.getItem('username') || '';
    this.getContacts();
    this.lastMessage = null;
  },
  data() {
    return {
      userName: '',
      rooms: [],
      messages: [],
      currentUserId: 1,
      contactsList: null,
      messagesLoaded: false,
      hideSideNav: true,
      roomName: '',
      limit: 50,
      groupView: true,
      offset: 0,
      lastMessage: null,
      messageActions: [
        {
          name: 'flagMessage',
          title: 'Flag Message',
        },
        {
          name: 'editMessage',
          title: 'Edit Message',
          onlyMe: true,
        },
        {
          name: 'replyMessage',
          title: 'Reply',
        },
        {
          name: 'deleteMessage',
          title: 'Delete Message',
          onlyMe: true,
        },
      ],
    };
  },
  methods: {
    async messageActionHandler({ roomId, action, message }) {
      try {
        const options = { roomId, message };
        switch (action.name) {
        case 'flagMessage':
          this.flagMessage(options);
          break;
        case 'editMessage':
          this.editMessage(options);
          break;
        case 'replyMessage':
          this.replyMessage(options);
          break;
        case 'deleteMessage':
          this.deleteMessage(options);
          break;
        default:
          break;
        }
      } catch (err) {
        console.error(err);
      }
    },
    async flagMessage({ roomId, message }) {
      try {
        const params = {
          roomId,
          messageId: message._id,
          firstName: message.sender_id,
          message: message.content,
          isGroup: this.groupView,
        };
        await MessageService.flagMessage(params);
      } catch (err) {
        console.error(err);
      }
    },
    async editMessage({ roomId, message }) {
      try {
        const params = {
          roomId,
          id: message._id,
          content: message.content,
        };
        await MessageService.editMessage(params);
      } catch (err) {
        console.error(err);
      }
    },
    async replyMessage({ roomId, message }) {
      try {
        const params = {};
        console.info('replyMessage', roomId, message);
      } catch (err) {
        console.error(err);
      }
    },
    async deleteMessage({ message }) {
      try {
        const params = {
          id: message._id,
        };
        await MessageService.deleteMessage(params);
      } catch (err) {
        console.error(err);
      }
    },
    async getContacts() {
      try {
        const data = await this.$http.get('/dialogs');
        this.contactsList = data.data.dialogs;
      } catch (err) {
        console.error(err);
      }
    },
    async loadOldMessages({
      room,
      options = {},
    }) {
      try {
        const {
          roomId,
        } = room;
        const {
          reset = false,
        } = options;
        this.messagesLoaded = false;
        if (this.messages.length < 50) {
          this.messagesLoaded = true;
          return;
        }
        if (reset) {
          return;
        }
        const {
          limit,
          lastMessage,
          groupView,
        } = this;
        let newMessages = [];
        const params = {
          roomId,
          limit,
          lazy: true,
        };
        if (groupView && lastMessage) {
          params.offset = lastMessage.id;
        } else {
          this.offset += 50;
          params.offset = this.offset;
        }
        if (groupView) {
          const data = await MessageService.fetchGroupMessages(params);
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
        } else {
          const data = await MessageService.getIndividualMessages(params);
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
        }
        if (!newMessages.length) {
          this.messagesLoaded = true;
          return;
        }
        const formattedMessages = [];
        const formattedRoomStructure = [];
        const users = [];
        newMessages.forEach((d) => {
          if (!groupView) {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
          }
          users.push({
            _id: d.id,
            username: d.sender,
          });
          formattedMessages.push({
            _id: d.id,
            content: d.message || '',
            sender_id: d.sender,
            date: dateHelpers.convertDate(d.date),
            timestamp: dateHelpers.convertTime(d.date),
          });
        });
        if (groupView) {
          [this.lastMessage] = newMessages;
        }
        formattedRoomStructure.push({
          roomId,
          roomName: room.roomName,
          users,
        });
        if (formattedMessages.length < 50) {
          this.messagesLoaded = true;
        }
        this.messages = [...formattedMessages, ...this.messages];
        this.rooms = formattedRoomStructure;
      } catch (err) {
        console.error(err);
      }
    },
    async getIndividualMessages({
      roomName,
      roomId,
    }) {
      try {
        this.messagesLoaded = false;
        this.offset = 0;
        const {
          limit,
          offset,
        } = this;
        const params = {
          roomId,
          limit,
          offset,
        };
        this.resetChatWidget();
        const data = await MessageService.getIndividualMessages(params);
        if (data.data.is_success) {
          this.groupView = false;
          const formattedMessages = [];
          const formattedRoomStructure = [];
          this.currentUserId = roomId;
          const newMessages = data.data.messages;
          if (newMessages.length < 50) {
            this.messagesLoaded = true;
          }
          newMessages.forEach((d) => {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
            formattedMessages.push({
              _id: d.id,
              content: d.message || '',
              sender_id: d.sender,
              date: dateHelpers.convertDate(d.date),
              timestamp: dateHelpers.convertTime(d.date),
            });
          });
          formattedRoomStructure.push({
            roomId,
            roomName,
            users: [],
          });
          this.messages = formattedMessages;
          this.rooms = formattedRoomStructure;
        }
      } catch (err) {
        console.error(err);
      }
    },
    async getGroupMessages({
      roomName,
      roomId,
      lazy = false,
    }) {
      try {
        const {
          limit,
          lastMessage,
        } = this;
        if (!this.groupView) {
          this.lastMessage = null;
        }
        this.groupView = true;
        const params = {
          roomId,
          limit,
        };
        if (this.messages.length && lazy && lastMessage) {
          params.offset = lastMessage.id;
        }
        this.resetChatWidget();
        const data = await MessageService.fetchGroupMessages(params);
        if (data && data.data.is_success) {
          this.currentUserId = '';
          const formattedMessages = [];
          const formattedRoomStructure = [];
          const userList = [];
          const newMessages = data.data.messages;
          if (newMessages.length < 50) {
            this.messagesLoaded = true;
          }
          newMessages.forEach((d) => {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
            this.roomName = d.sender;
            userList.push({
              _id: d.id,
              username: d.sender,
            });
            formattedMessages.push({
              _id: d.id || '',
              content: d.message || '',
              sender_id: d.sender || '',
              date: dateHelpers.convertDate(d.date),
              timestamp: dateHelpers.convertTime(d.date),
              username: this.roomName,
            });
          });
          formattedRoomStructure.push({
            roomId,
            roomName,
            users: userList,
          });
          this.messages = formattedMessages;
          this.rooms = formattedRoomStructure;
          [this.lastMessage] = newMessages;
        }
      } catch (err) {
        console.error(err);
      }
    },
    async sendMessage({
      roomId,
      content,
      file,
      replyMessage,
    }) {
      try {
        const response = await MessageService.addNewMessage({
          roomId,
          content,
          file,
          replyMessage,
        });
        if (response && response.status === 200) {
          this.messagesLoaded = false;
          const { message } = response.data;
          const { date } = message;
          const newMessages = [...this.messages, {
            _id: message.id,
            individual: roomId,
            content,
            sender_id: this.currentUserId,
            date: dateHelpers.convertDate(date),
            timestamp: dateHelpers.convertTime(date),
            username: this.sender,
          }];
          this.messages = newMessages;
          this.messagesLoaded = true;
        }
      } catch (err) {
        console.error(err);
      }
    },
    resetChatWidget() {
      this.rooms.length = 0;
      this.messages.length = 0;
      this.messagesLoaded = false;
      this.lastMessage = null;
      this.offset = 0;
    },
  },
};
</script>
