import Axios from 'axios';

let baseURL = 'http://localhost:8000/api/'

export const axios = Axios.create({
  baseURL: `${baseURL}`
})
