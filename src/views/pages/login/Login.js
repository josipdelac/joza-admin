import React, { useState } from 'react';
import { CButton, CForm, CFormInput, CInputGroup, CInputGroupText, CRow, CCol } from '@coreui/react';
import { cilLockLocked, cilUser } from '@coreui/icons';
import axios from 'axios'; // Import axios for making API requests

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogin = async () => {
    try {
      console.log("EJ OD KAD SAM SE RODIO")
      const response = await axios.post('http://localhost:5000/api/login', { username, password });

      // Handle successful login here (e.g., set user data in state, manage sessions)
      console.log('Login successful:', response.data);
    } catch (error) {
      setErrorMessage('Invalid credentials');
      console.error('Login failed:', error);
    }
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
            placeholder="Password"
            autoComplete="current-password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </CInputGroup>
        {errorMessage && <div className="text-danger">{errorMessage}</div>}
        <CRow>
          <CCol xs={6}>
            <Button  onClick={handleLogin}>
              Login
            </Button>
          </CCol>
        </CRow>
      </CForm>
    </div>
  );
};

export default Login;
