import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ChatUser } from '@/types/chatuser';

const initialState: Record<string, ChatUser[]> = {};

// Create the slice for domains
export const chatUserSlice = createSlice({
  name: 'chatuser',
  initialState,
  reducers: {
    addChatUsers: (state, action: PayloadAction<{ chatbot_uuid: string, users: ChatUser[] }>) => {
      const { chatbot_uuid, users } = action.payload;
      if (!state[chatbot_uuid]) {
        state[chatbot_uuid] = [];
      }
      users.forEach(user => {
        if(user) {
          if (!state[chatbot_uuid].some(existingUser => existingUser.uuid === user.uuid)) {
            state[chatbot_uuid].push(user);
          }
        }
      });
    },
  },
});

// Action creators are automatically generated
export const { addChatUsers } = chatUserSlice.actions;

// Export the reducer to be included in the store
export default chatUserSlice.reducer;
