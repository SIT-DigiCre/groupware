import { TextField, Grid, Card, Button } from "@mui/material";
import { useCallback, useState } from "react";
import { axios } from "../utils/axios";
import { baseURL } from "../utils/common";
import { useRouter } from "next/dist/client/router";

const LoginPage = () => {
  const router = useRouter();
  const [isError, setIsError] = useState(false);
  const [onLogin, setOnLogin] = useState(false);
  const [emailField, setEmailField] = useState("");
  const [passwdField, setPasswdField] = useState("");
  const handleOnChangeEmailField = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setEmailField(e.target.value);
    },
    []
  );
  const handleOnChangePasswdField = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setPasswdField(e.target.value);
    },
    []
  );
  const login = useCallback(() => {
    axios
      .post("/v1/auth/jwt/create", {
        email: emailField,
        password: passwdField,
      })
      .then((res) => {
        localStorage.setItem("jwt", res.data.access);
        localStorage.setItem("refresh-jwt", res.data.refresh);
        axios
          .get("/v1/account/userinfo/", {
            headers: {
              Authorization: "JWT " + res.data.access,
            },
          })
          .then((rtn) => {
            localStorage.setItem("user-info", JSON.stringify(rtn.data[0]));
            router.push("/");
          })
          .catch((error) => console.log(error));
      })
      .catch((error) => {
        if (error.response.status === 401) setIsError(true);
      });
  }, [emailField, passwdField, router]);
  return (
    <Grid
      container
      alignItems="center"
      justifyContent="center"
      className="mt-2"
    >
      <Grid item xs={8}>
        <Card style={{ padding: "10px" }}>
          <h1 className="text-center">デジコアログイン</h1>
          <TextField
            label="Email"
            type="email"
            fullWidth
            error={isError}
            onChange={handleOnChangeEmailField}
            variant="standard"
          />
          <TextField
            label="Password"
            type="password"
            fullWidth
            error={isError}
            onChange={handleOnChangePasswdField}
            variant="standard"
          />
          {isError ? (
            <p style={{ color: "red" }}>
              メールアドレスかパスワードが間違っています
            </p>
          ) : null}
          <Button
            variant="contained"
            color="primary"
            fullWidth
            className="mt-2"
            onClick={login}
          >
            ログイン
          </Button>
        </Card>
      </Grid>
    </Grid>
  );
};

export default LoginPage;
