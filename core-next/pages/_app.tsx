import Head from "next/head";
import { Component } from "react";
import Drawer from "../components/Drawer";
import "highlightjs/styles/vs2015.css";
import "../styles/common.css";
import dynamic from "next/dynamic";

const LoginCheck = dynamic(() => import("../components/LoginCheck"), {
  ssr: false,
});

const App = ({ Component, pageProps }) => {
  return (
    <div>
      <LoginCheck />
      <Head children={""}></Head>
      <Drawer>
        <Component {...pageProps} />
      </Drawer>
    </div>
  );
};
export default App;
