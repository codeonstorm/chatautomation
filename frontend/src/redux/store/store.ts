import { configureStore } from '@reduxjs/toolkit'
import userReducer from './features/user/user'
import domainReducer from './features/domain/domain'
import chatbotReducer from './features/chatbot/chatbot'
import chatUserReducer from './features/chathistory/chathistory'
import scrapedUrlReducer from './features/scrapedurl/scrapedurl'
import webhookReducer from './features/webhook/webhook'

export const makeStore = () => {
  return configureStore({
    reducer: {
      user: userReducer,
      domains: domainReducer,
      chatbots: chatbotReducer,
      chatuser: chatUserReducer,
      scrapedurls: scrapedUrlReducer,
      webhook: webhookReducer
    },
  })
}

// Infer the type of makeStore
export type AppStore = ReturnType<typeof makeStore>
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']