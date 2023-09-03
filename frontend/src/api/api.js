import axios from "axios"
import CryptoJS from "crypto-js";



const API_URL= "http://127.0.0.1:8001";


export const useGetRobotStatus = async (id) => {
    const config = {
        headers:{
            "Authorization" : `Bearer ${localStorage.getItem(token)}`
        } 
    }
    const result = await axios.get(`${API_URL}/entries/`,config);
    console.log("ALL ENTRIES", result)
    return result;
};
//Function to Convert hex to bytes
const hexToBytes = (hex) => {
    var bytes = [];
  
    for (var c = 0; c < hex.length; c += 2) {
      bytes.push(parseInt(hex.substr(c, 2), 16));
    }
  
    return bytes;
  };

 
export const useGetRobotStatusLastEntry = async (id) => {
    const config = {
        headers:{
            "Authorization" : `Bearer ${localStorage.getItem(token)}`
        } 
    }
    const result = await axios.get(`${API_URL}/last_entry/${id}`,config);
    
    const key = process.env.REACT_APP_AES_ENCRYPTION_KEY;
    console.log("Key",key)
    const secretPass = hexToBytes(key)
    console.log("Secret Pass",result,key,secretPass)
    const bytes = CryptoJS.AES.decrypt(result.data, key);
    console.log("Decrypted",bytes.toString(CryptoJS.enc.Utf8),bytes.toString(CryptoJS.enc.Utf8))
    const data = JSON.parse(bytes.toString(CryptoJS.enc.Utf8));

    return data;
};

export const useGetProcessedItems = async (type) => {
    const config = {
        headers:{
            "Authorization" : `Bearer ${localStorage.getItem(token)}`
        } 
    }
    const result = await axios.get(`${API_URL}/sum_total_items/${type}`,config);
    return result;
};

export const useGetRobotsStatusLastEntries = async () => {
    const config = {
        headers:{
            "Authorization" : `Bearer ${localStorage.getItem(token)}`
        } 
    }
    const result = await axios.get(`${API_URL}/last_entries/`,config);
    return result;
};