import React, { useState } from 'react';
import { CButton, CForm, CFormInput, CInputGroup, CInputGroupText, CRow, CCol } from '@coreui/react';
import { cilLockLocked, cilUser } from '@coreui/icons';
import axios from 'axios'; // Import axios for making API requests

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // Ovdje dodajte logiku za prijavu
  };

  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CForm>
        <CInputGroup className="mb-3">
          <CInputGroupText>
            <CIcon icon={cilUser} />
          </CInputGroupText>
          <CFormInput
            placeholder="Username"
            autoComplete="username"
            onChange={(e) => setUsername(e.target.value)}
          />
        </CInputGroup>
        <CInputGroup className="mb-4">
          <CInputGroupText>
            <CIcon icon={cilLockLocked} />
          </CInputGroupText>
          <CFormInput
            type="password"
            placeholder="TESTTTTTT"
            autoComplete="current-password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </CInputGroup>
        <CRow>
          <CCol xs={6}>
            <button  onclick={() => {console.log("Pozvanp,,,,,"); handleLogin();}}>
              Login
            </button>
          </CCol>
        </CRow>
      </CForm>
    </div>
  );
};

export default Login;
