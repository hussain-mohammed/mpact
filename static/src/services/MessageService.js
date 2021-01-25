import Api from './Api';

export default {
  async addNewMessage({
    roomId,
    content,
  }) {
    try {
      const result = await Api.post('/message', {
        individual: roomId,
        message: content,
      });
      return result;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async getIndividualMessages({
    roomId,
    offset,
    limit = 50,
  }) {
    try {
      const result = await Api.get(`message/individual/${roomId}`, {
        params: {
          offset,
          limit,
        },
      });
      return result;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
  async fetchGroupMessages({
    roomId,
  }) {
    try {
      const result = await Api.get(`message/chat/${roomId}`);
      return result;
    } catch (err) {
      console.error(err);
      throw err;
    }
  },
};
