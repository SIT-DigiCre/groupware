import Head from "next/head";
import { Component } from "react";
import Drawer from "../components/Drawer";
import "highlightjs/styles/vs2015.css";
import "../styles/common.css";
import dynamic from "next/dynamic";
import { Provider } from "react-redux";
import { persistStore } from "redux-persist";
import { PersistGate } from "redux-persist/integration/react";
import { useStore } from "../store";

const LoginCheck = dynamic(() => import("../components/LoginCheck"), {
  ssr: false,
});

const App = ({ Component, pageProps }) => {
  const store = useStore();
  const persistor = persistStore(store);
  return (
    <Provider store={store}>
      <PersistGate persistor={persistor}>
        <LoginCheck />
        <Head children={""}></Head>
        <Drawer>
          <Component {...pageProps} />
        </Drawer>
      </PersistGate>
    </Provider>
  );
};
export default App;
