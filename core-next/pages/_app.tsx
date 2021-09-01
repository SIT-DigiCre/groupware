import Head from 'next/head';
import Header from '../components/Header';
import { Component } from 'react';
import Drawer from '../components/Drawer';
import 'highlightjs/styles/vs2015.css';
import 'bootstrap/dist/css/bootstrap.min.css';
//import '../styles/common.css'

const App = ({ Component, pageProps }) => {
  return (
    <div>
      <Head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans+JP&subset=japanese" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
      </Head>
      <Drawer>
        <Component {...pageProps} />
      </Drawer>
    </div>
  );
}
export default App