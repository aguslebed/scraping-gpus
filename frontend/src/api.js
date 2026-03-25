import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

export const getGpus = async () => {
  const response = await api.get('/gpus');
  return response.data;
};

export const getPrices = async () => {
  const response = await api.get('/prices');
  return response.data;
};
