import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AppFooter, AppHeader,AppSidebar, AppBreadcrumb } from 'src/components';
import {useNavigate } from 'react-router-dom';
import LanguageContext from 'src/components/localizationContext'

function Logs() {
  const [logs, setLogs] = useState([]);
  const [updateLogData, setUpdateLogData] = useState({});
  const [deleteLogId, setDeleteLogId] = useState(null);
  const value = useContext(LanguageContext);  


  useEffect(() => {
    getLogs();
  }, []);

  const getLogs = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/logs');
      setLogs(response.data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  

  const updateLog = async (logId) => {
    try {
      await axios.put(`http://localhost:5000/api/logs/${logId}`, updateLogData);
      setUpdateLogData({});
      getLogs();
    } catch (error) {
      console.error('Error updating log:', error);
    }
  };

  const deleteLog = async () => {
    if (deleteLogId) {
      try {
        await axios.delete(`http://localhost:5000/api/logs/delete/${deleteLogId}`);
        setDeleteLogId(null);
        getLogs();
      } catch (error) {
        console.error('Error deleting log:', error);
      }
    }
  };

  return (
    <div>
      <AppHeader />
      <h2>{value.logmanagment}</h2>

  
      

      {/* Dodajte listu logova */}
      <div>
        <h3>{value.log}</h3>
        <ul>
        {logs.map((log) => (
            <li key={log.user_id}>
                Action: {log.action}<br />
                Timestamp: {log.timestamp}<br />
                User ID: {log.user_id}<br />
                Deleted By: {log.deleted_by}<br />
                <button onClick={() => setUpdateLogData({ id: log.user_id })}>Edit</button>
                <button onClick={() => setDeleteLogId(log.user_id)}>Delete</button>
            </li>
            ))}
        </ul>
      </div>

      {/* Dodajte formu za uređivanje loga */}
      {updateLogData.id && (
        <div>
          <h3>Edit Log</h3>
          <input
            type="text"
            placeholder="Action"
            value={updateLogData.action || ''}
            onChange={(e) => setUpdateLogData({ ...updateLogData, action: e.target.value })}
          />
          <input
            type="text"
            placeholder="Timestamp"
            value={updateLogData.timestamp || ''}
            onChange={(e) => setUpdateLogData({ ...updateLogData, timestamp: e.target.value })}
          />
          <button onClick={() => updateLog(updateLogData.id)}>Update Log</button>
        </div>
      )}

      {/* Dodajte formu za brisanje loga */}
      {deleteLogId && (
        <div>
          <h3>Delete Log</h3>
          <p>Are you sure you want to delete this log?</p>
          <button onClick={deleteLog}>Delete Log</button>
        </div>
      )}
    </div>
  );
}

export default Logs;
