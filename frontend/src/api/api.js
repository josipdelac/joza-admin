import axios from 'axios'
import CryptoJS from 'crypto-js'
import { useNavigate } from 'react-router-dom';


const API_URL = 'http://127.0.0.1:8001'
const APP_URL = 'http://127.0.0.1:5000'

export const useGetRobotStatus = async (id) => {
  const config = {
    headers: {
      Authorization: `Bearer ${localStorage['token']}`,
    },
  }
  const result = await axios.get(`${API_URL}/entries/`, config)
  console.log('ALL ENTRIES', result)
  return result
}
//Function to Convert hex to bytes
const hexToBytes = (hex) => {
  var bytes = []

  for (var c = 0; c < hex.length; c += 2) {
    bytes.push(parseInt(hex.substr(c, 2), 16))
  }

  return bytes
}

export const useGetRobotStatusLastEntry = async (id) => {
  const config = {
    headers: {
      Authorization: `Bearer ${localStorage['token']}`,
    },
  }
  const bs = await axios.get(`${API_URL}/last_entry/${id}`, config)
    const data = bs.data

  return data
}

export const useGetProcessedItems = async (type) => {
  const config = {
    headers: {
      Authorization: `Bearer ${localStorage['token']}`,
    },
  }
  const result = await axios.get(`${API_URL}/sum_total_items/${type}`, config)
  return result
}

export const useGetCurrentUser = async () => {
  const config = {
    headers: {
      Authorization: `Bearer ${localStorage['token']}`,
      'authorization': "Bearer " + localStorage['token'],
    },
  }
  console.log('Current User',config.headers)
  const result = await axios.get(`${APP_URL}/api/get_user`, config)
  return result
}

export const useGetRobotsStatusLastEntries = async () => {
  const token = localStorage['token'] || ''
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
  const result = await axios.get(`${API_URL}/last_entries/`, config)
  return result
}

export const fetchData = async () => {
  const token = localStorage['token'] || ''
  const config = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
  const result = await axios.get(`${APP_URL}/api/users`, config)
  return result
}


