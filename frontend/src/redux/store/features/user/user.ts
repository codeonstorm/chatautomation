import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { User } from '@/types/user'

// Fix: state is nullable (e.g. no user logged in yet)
// const initialState: User | null = null;

export const userSlice = createSlice({
  name: 'user',
  initialState: null as User | null,
  reducers: {
    setUser(_state, action: PayloadAction<User>) {
      return action.payload
    },
    removeUser() {
      return null
    },
    updateUser(state, action: PayloadAction<Partial<User>>) {
      if (state) {
        return { ...state, ...action.payload }
      }
      return state
    }
  }
})

export const { setUser, removeUser, updateUser } = userSlice.actions
export default userSlice.reducer