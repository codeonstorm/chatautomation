import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { User } from '@/types/user'

// Fix: state is nullable (e.g. no user logged in yet)
const initialState: User  = null

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<User>) {
      return action.payload
    },
    removeUser() {
      return null
    },
    updateUser(state, action: PayloadAction<Partial<User>>) {
      if (state) {
        return { ...state, ...action.payload }
      }
    }
  }
})

export const { setUser, removeUser, updateUser } = userSlice.actions
export default userSlice.reducer
