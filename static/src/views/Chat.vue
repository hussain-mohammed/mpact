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
         @send-message='sendMessages($event)' />
      </div>
    </div>
  </div>
</template>

<script>
import MessageService from '../services/MessageService';
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
      lastMessage: null,
    };
  },
  methods: {
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
        };
        if (lastMessage) {
          params.offset = lastMessage.id;
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
        if (newMessages.length === 0) {
          this.messagesLoaded = true;
          return;
        }
        this.currentUserId = roomId;
        const formattedMessages = [];
        const formattedRoomStructure = [];
        newMessages.forEach((d) => {
          if (d.individual !== d.sender) {
            this.currentUserId = d.sender;
          }
          formattedMessages.push({
            _id: d.id,
            id: d.id,
            content: d.message || '',
            sender_id: d.sender,
            date: this.convertDate(d.date),
            timestamp: this.convertTime(d.date),
          });
        });
        this.lastMessage = newMessages[newMessages.length - 1];
        formattedRoomStructure.push({
          roomId,
          roomName: room.roomName,
          users: [],
        });
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
        const {
          limit,
          lastMessage,
        } = this;
        const params = {
          roomId,
          limit,
        };
        if (!this.groupView && lastMessage) {
          params.offset = lastMessage.id;
        }
        const data = await MessageService.getIndividualMessages(params);
        if (data.data.is_success) {
          this.groupView = false;
          this.resetChatWidget();
          const formattedMessages = [];
          const formattedRoomStructure = [];
          this.currentUserId = roomId;
          const newMessages = data.data.messages;
          newMessages.forEach((d) => {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
            formattedMessages.push({
              _id: d.id,
              id: d.id,
              content: d.message || '',
              sender_id: d.sender,
              date: this.convertDate(d.date),
              timestamp: this.convertTime(d.date),
            });
          });
          formattedRoomStructure.push({
            roomId,
            roomName,
            users: [],
          });
          this.messages = formattedMessages;
          this.rooms = formattedRoomStructure;
          this.lastMessage = newMessages[newMessages.length - 1];
        }
      } catch (err) {
        console.error(err);
      }
    },
    async getGroupMessages({
      roomName,
      roomId,
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
        if (this.groupView && lastMessage) {
          params.offset = lastMessage.id;
        }
        this.messagesLoaded = false;
        const data = await MessageService.fetchGroupMessages(params);
        if (data && data.data.is_success) {
          this.resetChatWidget();
          this.currentUserId = '';
          const formattedMessages = [];
          const formattedRoomStructure = [];
          const userList = [];
          const newMessages = data.data.messages;
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
              date: this.convertDate(d.date),
              timestamp: this.convertTime(d.date),
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
    async sendMessages({
      roomId,
      content,
      file,
      replyMessage,
    }) {
      try {
        const data = await MessageService.addNewMessage({
          roomId,
          content,
          file,
          replyMessage,
        });
        if (data && data.status === 200) {
          this.messagesLoaded = false;
          const newMessages = [...this.messages, {
            _id: Math.random().toString(32).slice(2),
            individual: roomId,
            content,
            sender_id: this.currentUserId,
            date: this.convertDate(new Date()),
            timestamp: this.convertTime(new Date()),
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
    },
    convertDate(date) {
      const dateString = new Date(date);
      let month = `${dateString.getMonth() + 1}`;
      let day = `${dateString.getDate()}`;
      const year = dateString.getFullYear();
      if (month.length < 2) month = `0${month}`;
      if (day.length < 2) day = `0${day}`;
      return [day, month, year].join('-');
    },
    convertTime(time) {
      const timeString = new Date(time);
      return `${timeString.getHours()}:${timeString.getMinutes()}`;
    },
  },
};
</script>
