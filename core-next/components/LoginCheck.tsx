import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../store";
import { tokenSlice } from "../store/token";
import { useRouter } from "next/dist/client/router";
import axios from "axios";
import { baseURL } from "../utils/common";
import { useEffect } from "react";
const LoginCheck = () => {
  const dispatch = useDispatch();
  const token = useSelector((state: RootState) => state.token);
  const router = useRouter();

  useEffect(() => {
    if (router.pathname !== "/login") {
      if (token.token.jwt == null) {
        router.push("/login");
        return;
      }
      axios
        .post(baseURL + "/api/v1/auth/jwt/verify", {
          token: token.token.jwt,
        })
        .catch((error) =>
          axios
            .post(baseURL + "/api/v1/auth/jwt/refresh", {
              refresh: token.token.refresh,
            })
            .then((res: any) => {
              dispatch(
                tokenSlice.actions.updateToken({
                  jwt: res.data.access,
                  refresh: token.token.refresh,
                })
              );
            })
            .catch((error) => {
              router.push("/login");
            })
        );
    }
  }, []);
  return <></>;
};

export default LoginCheck;
