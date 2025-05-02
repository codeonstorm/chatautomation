import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ChatUser } from '@/types/chatuser';

const initialState: ChatUser[] = [];

// Create the slice for domains
export const chatUserSlice = createSlice({
  name: 'chatuser',
  initialState,
  reducers: {
    addChatUsers: (state, action: PayloadAction<ChatUser[]>) => {
      state.push(...action.payload);
    },
  },
});

// Action creators are automatically generated
export const { addChatUsers } = chatUserSlice.actions;

// Export the reducer to be included in the store
export default chatUserSlice.reducer;
