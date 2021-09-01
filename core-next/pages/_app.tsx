import Header from '../components/Header'
import { Component } from 'react';
import 'highlightjs/styles/vs2015.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/common.css'

const App = ({ Component, pageProps }) => {
  return (
    <div>
      <Header/>
      <Component {...pageProps} />
    </div>
  );
}
export default App