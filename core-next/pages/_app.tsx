import Head from 'next/head';
import Header from '../components/Header';
import { Component } from 'react';
import Drawer from '../components/Drawer';
import 'highlightjs/styles/vs2015.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/common.css'

const App = ({ Component, pageProps }) => {
  return (
    <div>
      <Head>
      </Head>
      <Drawer>
        <Component {...pageProps} />
      </Drawer>
    </div>
  );
}
export default App