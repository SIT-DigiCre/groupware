import Header from '../components/Header'
import { AppProps } from 'next/dist/next-server/lib/router/router';
import { Component } from 'react';
import Head from 'next/head';
import 'highlightjs/styles/vs2015.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = ({ Component, pageProps }: AppProps) => {
  return (
    <div>
      <Head>
      </Head>
      <Header/>
      <Component {...pageProps} />
    </div>
  );
}
export default App