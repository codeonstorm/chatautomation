import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Webhook, StatusEnum, WebhookState } from '@/types/webhook'


const initialState: WebhookState = {};

export const webhookSlice = createSlice({
  name: 'webhook',
  initialState,
  reducers: {
    setWebhook: (state, action: PayloadAction<{ chatbot_uuid: string, webhook: Webhook }>) => {
      const { chatbot_uuid, webhook } = action.payload;
      state[chatbot_uuid] = webhook;
    },
    removeWebhook: (state, action: PayloadAction<{ chatbot_uuid: string }>) => {
      const { chatbot_uuid } = action.payload;
      delete state[chatbot_uuid];
    },
  },
});

export const { setWebhook } = webhookSlice.actions;
export default webhookSlice.reducer;
