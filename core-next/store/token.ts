import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type Token = {
  jwt: string | null;
  refresh: string | null;
};
export type TokenState = {
  token: Token;
};

const initialState: TokenState = {
  token: {
    jwt: null,
    refresh: null,
  }
};

export const tokenSlice = createSlice({
  name: "token",
  initialState,
  reducers: {
    updateToken(state, action: PayloadAction<Token>) {
      state.token = action.payload;
    },
    reset(state) {
      state.token = initialState.token;
    },
  },
});
