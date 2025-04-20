import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Chatbot } from '@/types/chatbot';

const initialState: Chatbot[] = [];

// Create the slice for chatbots
export const chatbotSlice = createSlice({
  name: 'chatbots',
  initialState,
  reducers: {
    addChatbots: (state, action: PayloadAction<Chatbot[]>) => {
      state.push(...action.payload);
    },
    editChatbot: (state, action: PayloadAction<Chatbot>) => {
      const index = state.findIndex(chatbot => chatbot.uuid === action.payload.uuid);
      if (index !== -1) {
        state[index] = action.payload;
      }
    },
    removeChatbot: (state, action: PayloadAction<string>) => {
      return state.filter(chatbot => chatbot.uuid !== action.payload);
    },    
  },
});

// Action creators are automatically generated
export const { addChatbots, editChatbot, removeChatbot } = chatbotSlice.actions;

// Export the reducer to be included in the store
export default chatbotSlice.reducer;
