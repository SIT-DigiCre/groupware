import { useRouter } from "next/dist/client/router";
import axios from "axios";
import { baseURL } from "../utils/common";
import { useEffect } from "react";
const LoginCheck = () => {
  const router = useRouter();

  useEffect(() => {
    if (router.pathname !== "/login") {
      if (localStorage.getItem("jwt") == null) {
        router.push("/login");
        return;
      }
      axios
        .post(baseURL + "/api/v1/auth/jwt/verify", {
          token: localStorage.getItem("jwt"),
        })
        .catch((error) =>
          axios
            .post(baseURL + "/api/v1/auth/jwt/refresh", {
              refresh: localStorage.getItem("refresh-jwt"),
            })
            .then((res: any) => {
              localStorage.setItem("jwt", res.data.access);
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
