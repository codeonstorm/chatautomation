import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ScrapedUrls } from '@/types/scrapedurls';

const initialState: ScrapedUrls[] = [];

export const scrapedUrls = createSlice({
  name: 'scrapedurls',
  initialState,
  reducers: {
    addUrl: (state, action: PayloadAction<ScrapedUrls[]>) => {
      action.payload.forEach(url => {
        if (!state.some(existingUrl => existingUrl.id === url.id)) {
          state.push(url);
        }
      });
    },
  },
});

// Action creators are automatically generated
export const { addUrl } = scrapedUrls.actions;

// Export the reducer to be included in the store
export default scrapedUrls.reducer;
