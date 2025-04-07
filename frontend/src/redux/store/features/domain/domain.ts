import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Domain } from '@/types/domain';

const initialState: Domain[] = [];

// Create the slice for domains
export const domainSlice = createSlice({
  name: 'domains',
  initialState,
  reducers: {
    add: (state, action: PayloadAction<Domain>) => {
      state.push(action.payload); // Push the domain passed in the action payload
    },
    addDomains: (state, action: PayloadAction<Domain[]>) => {
      state.push(...action.payload); // Spread the array of domains into the state
    },
    remove: (state, action: PayloadAction<string>) => {
      const index = state.findIndex(domain => domain.uuid === action.payload);
      if (index !== -1) {
        state.splice(index, 1);
      }
    },
  },
});

// Action creators are automatically generated
export const { add, addDomains, remove } = domainSlice.actions;

// Export the reducer to be included in the store
export default domainSlice.reducer;
