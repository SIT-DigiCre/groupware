import axiosBase from "axios";

const isProduction = process.env.NODE_ENV === "production";

export const axios = axiosBase.create({
  baseURL: isProduction ? 'https://core.digicre.net/api' : 'http://localhost:8000/api',
  headers:{
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  responseType: 'json'
});