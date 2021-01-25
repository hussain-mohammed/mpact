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
      offset: 0,
      limit: 50,
      groupView: true,
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
        this.messagesLoaded = false;
        const {
          roomId,
        } = room;
        const {
          reset = false,
        } = options;
        if (reset) {
          this.offset = 50;
          return;
        }
        const {
          offset,
          limit,
        } = this;
        let newMessages = [];
        if (this.groupView) {
          const data = await MessageService.fetchGroupMessages({
            roomId,
            offset,
            limit,
          });
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
        } else {
          const data = await MessageService.getIndividualMessages({
            roomId,
            offset,
            limit,
          });
          if (data.data.is_success) {
            newMessages = data.data.messages;
          }
        }
        this.currentUserId = roomId;
        const formattedMessages = [];
        const formattedRoomStructure = [];
        this.offset += this.limit;
        if (newMessages.length === 0) {
          this.messagesLoaded = true;
          return;
        }
        newMessages.forEach((d) => {
          if (d.individual !== d.sender) {
            this.currentUserId = d.sender;
          }
          formattedMessages.push({
            _id: Math.random() * 1000,
            content: d.message || '',
            sender_id: d.sender,
            date: this.convertDate(d.date),
            timestamp: this.convertTime(d.date),
          });
        });
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
        const {
          offset,
          limit,
        } = this;
        const data = await MessageService.getIndividualMessages({
          roomId,
          offset,
          limit,
        });
        if (data.data.is_success) {
          this.groupView = false;
          this.offset += this.limit;
          this.resetChatWidget();
          const formattedMessages = [];
          const formattedRoomStructure = [];
          this.currentUserId = roomId;
          data.data.messages.forEach((d) => {
            if (d.individual !== d.sender) {
              this.currentUserId = d.sender;
            }
            formattedMessages.push({
              _id: Math.random() * 1000,
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
          offset,
          limit,
        } = this;
        const data = await MessageService.fetchGroupMessages({
          roomId,
          offset,
          limit,
        });
        if (data && data.data.is_success) {
          this.resetChatWidget();
          this.currentUserId = '';
          const formattedMessages = [];
          const formattedRoomStructure = [];
          const userList = [];
          data.data.messages.forEach((d) => {
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