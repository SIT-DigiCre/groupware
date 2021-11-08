import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../store";
import { tokenSlice } from "../store/token";
import { userInfoSlice } from "../store/user";
import { useRouter } from "next/dist/client/router";
import { axios } from "../utils/axios";
import { useEffect } from "react";
const LoginCheck = () => {
  const dispatch = useDispatch();
  const token = useSelector((state: RootState) => state.token.token);
  const user = useSelector((state: RootState) => state.user.user);
  const router = useRouter();

  useEffect(() => {
    if (router.pathname !== "/login") {
      if (token.jwt == null) {
        userInfoSlice.actions.reset();
        router.push("/login?redirect=" + router.pathname);
      } else {
        axios
          .post("/v1/auth/jwt/verify", {
            token: token.jwt,
          })
          .then(res=>console.log("TOKEN問題なし"))
          .catch((error) =>
            axios
              .post("/v1/auth/jwt/refresh", {
                refresh: token.refresh,
              })
              .then((res: any) => {
                dispatch(
                  tokenSlice.actions.updateToken({
                    jwt: res.data.access,
                    refresh: token.refresh,
                  })
                );
              })
              .catch((error) => {
                userInfoSlice.actions.reset();
                router.push("/login?redirect=" + router.pathname);
              })
          );
      }
    }
  }, []);
  return <></>;
};

export default LoginCheck;
