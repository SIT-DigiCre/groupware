import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserInfo } from "../interfaces/account";

export type UserState = {
  user: UserInfo;
};

const initialState: UserState = {
  user: {
    id: -1,
    username: "",
    email: "",
    student_id: "",
    icon: "",
  },
};

export const userInfoSlice = createSlice({
  name: "userInfo",
  initialState,
  reducers: {
    updateUser(state, action: PayloadAction<UserInfo>) {
      state.user = action.payload;
    },
    reset() {
      return initialState;
    },
  },
});
