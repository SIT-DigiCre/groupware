import { useRouter } from "next/dist/client/router";
import axios from "axios";
import { baseURL } from "../utils/common";
import { useEffect } from "react";
const LoginCheck = () => {
  const router = useRouter();

  useEffect(() => {
    if (router.pathname !== "/login") {
      console.log(localStorage.getItem("jwt"));
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
            .catch((error) => {
              router.push("/login");
            })
            .then((res: any) => {
              console.log(res.data);
              localStorage.setItem("jwt", res.data.access);
            })
        );
    }
  }, []);
  return <div></div>;
};

export default LoginCheck;
