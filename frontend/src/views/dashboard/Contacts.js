import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import {
    CButton,
    CCol,
    CContainer,
    CFormInput,
    CInputGroup,
    CInputGroupText,
    CRow,
    CAlert,
    CCard,
    CCardBody,
    CCardGroup,
    CForm,
  } from '@coreui/react'
  import CIcon from '@coreui/icons-react'
  import { cilFile, cilFolderOpen, cilLockLocked, cilUser } from '@coreui/icons'
  
  import { cilMagnifyingGlass } from '@coreui/icons'
  
  import { AppFooter, AppHeader,AppSidebar, AppBreadcrumb } from 'src/components';
  import LanguageContext from 'src/components/localizationContext'

function App() {
  const [users, setUsers] = useState([]);
  const [updateUserId, setUpdateUser] = useState({ id: '', email: '' });
  const [deleteUserId, setDeleteUserId] = useState('');
  const value = useContext(LanguageContext);  


  useEffect(() => {
    getUsers1();
  }, []);

  const getUsers1 = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/xmlusers');
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };



  const updateUser = async () => {
    try {
      await axios.put(`http://localhost:5000/api/xmlusers/update/${updateUserId.id}`, { email: updateUserId.email });
      setUpdateUser({ id: '', email: '' });
      getUsers1();
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  const deleteUser = async () => {
    try {
      await axios.delete(`http://localhost:5000/api/xmlusers/delete/${deleteUserId}`);
      setDeleteUserId('');
      getUsers1();
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <div >
    <AppHeader />
      

      <div>
        <h2>{value.updateuser}</h2>
        <input
          type="text"
          placeholder="User ID"
          value={updateUserId.id}
          onChange={(e) => setUpdateUser({ ...updateUserId, id: e.target.value })}
        />
        <input
          type="text"
          placeholder="New Email"
          value={updateUserId.email}
          onChange={(e) => setUpdateUser({ ...updateUserId, email: e.target.value })}
        />
        <button onClick={updateUser}>{value.updateuser}</button>
      </div>

      <div>
        <h2>{value.deleteuser}</h2>
        <input
          type="text"
          placeholder="User ID"
          value={deleteUserId}
          onChange={(e) => setDeleteUserId(e.target.value)}
        />
        <button onClick={deleteUser}>{value.deleteuser}</button>
      </div>

      <div>
        <h2>{value.users}</h2>
        <pre>{JSON.stringify(users, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
