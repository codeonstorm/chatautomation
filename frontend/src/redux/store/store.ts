import { configureStore } from '@reduxjs/toolkit'
import domainReducer from './features/domain/domain'


// don't do this as global in next js

// export const store = configureStore({
//   reducer: {
//     domain: domainReducer,
//   },
// })

// // Infer the `RootState` and `AppDispatch` types from the store itself
// export type RootState = ReturnType<typeof store.getState>
// // Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
// export type AppDispatch = typeof store.dispatch


export const makeStore = () => {
  return configureStore({
    reducer: {
      domains: domainReducer,
    },
  })
}

// Infer the type of makeStore
export type AppStore = ReturnType<typeof makeStore>
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']