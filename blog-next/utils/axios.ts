import axiosBase from 'axios';
import { baseURL } from './common'

export const axios = axiosBase.create({
  baseURL: baseURL + '/api',
  headers:{
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  responseType: 'json'
});