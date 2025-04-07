import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Define the state type
interface CounterState {
  value: number;
}

// Initial state
const initialState: CounterState = {
  value: 0,
};

// Create the counter slice
const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    setCounter: (state, action: PayloadAction<number>) => {
      state.value = action.payload;
    },
  },
});

// Export actions for use in components
export const { increment, decrement, setCounter } = counterSlice.actions;

// Export the reducer to be used in the store
export default counterSlice.reducer;
