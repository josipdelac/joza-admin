import axios from "axios"

const API_URL= "http://127.0.0.1:8001";


export const useGetRobotStatus = async (id) => {
    const result = await axios.get(`${API_URL}/entries/`);
    console.log("ALL ENTRIES", result)
    return result;
};

export const useGetRobotStatusLastEntry = async (id) => {
    const result = await axios.get(`${API_URL}/last_entry/${id}`);
    return result;
};

export const useGetRobotsStatusLastEntries = async () => {
    const result = await axios.get(`${API_URL}/last_entries/`);
    return result;
};