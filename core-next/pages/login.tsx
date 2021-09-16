import { TextField, Grid, Card, Button } from "@material-ui/core";
import { useState } from "react";
import axios from "axios";
import { baseURL } from "../utils/common";
import { useRouter } from "next/dist/client/router";

const LoginPage = () => {
  const router = useRouter();
  const [isError, setIsError] = useState(false);
  const [onLogin, setOnLogin] = useState(false);
  const [emailField, setEmailField] = useState("");
  const [passwdField, setPasswdField] = useState("");
  const handleOnChangeEmailField = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmailField(e.target.value);
  };
  const handleOnChangePasswdField = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setPasswdField(e.target.value);
  };
  const login = () => {
    axios
      .post(baseURL + "/api/v1/auth/jwt/create", {
        email: emailField,
        password: passwdField,
      })
      .then((res) => {
        localStorage.setItem("jwt", res.data.access);
        localStorage.setItem("refresh-jwt", res.data.refresh);
        router.push("/");
      })
      .catch((error) => {
        if (error.response.status === 401) setIsError(true);
      });
  };
  return (
    <Grid container alignItems="center" justify="center" className="mt-2">
      <Grid item xs={8}>
        <Card style={{ padding: "10px" }}>
          <h1 className="text-center">ﾛｸﾞｲﾝ</h1>
          <TextField
            label="Email"
            type="email"
            fullWidth
            error={isError}
            onChange={handleOnChangeEmailField}
          />
          <TextField
            label="Password"
            type="password"
            fullWidth
            error={isError}
            onChange={handleOnChangePasswdField}
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
            ﾛｸﾞｲﾝ
          </Button>
        </Card>
      </Grid>
    </Grid>
  );
};

export default LoginPage;
