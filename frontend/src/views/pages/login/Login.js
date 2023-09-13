import React, {useState, useEffect, useContext} from 'react'
import { Link } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser } from '@coreui/icons'
import axios from 'axios'
import {useNavigate } from 'react-router-dom';
import LanguageContext from 'src/components/localizationContext'




function Login(props) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [ipAddress, setIPAddress] = useState('');
  const navigate = useNavigate();
  const value = useContext(LanguageContext);  
  //console.log("Context", value)
 // const navigate = useNavigate();
  const {setUser} = props;
  const handleLogin = async () => {
    try {
      const data = {
        email,
        password,
        ipAddress,
      };

      const response = await axios.post('http://localhost:5000/api/login', data);

      if (response.data.message === 'User logged in successfully') {
        alert(response.data.message);
        localStorage.setItem("token",response.data.jwt)
        setUser(response.data.user_details)
        navigate('/dashboard'); // Preusmjeri korisnika na dashboard nakon prijave
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  
    
  
    useEffect(() => {
      fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => setIPAddress(data.ip))
        .catch(error => console.log(error))
    }, []);
  
    const localization= useContext('lo')

  

  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={8}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm>
                    <h1>{value.login}</h1>
                    <p className="text-medium-emphasis">{value.signin}</p>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilUser} />
                      </CInputGroupText>
                      <CFormInput type="email" 
                                  value={email} onChange={(e) => setEmail(e.target.value)} placeholder="e-mail" autoComplete="username" />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupText>
                        <CIcon icon={cilLockLocked} />
                      </CInputGroupText>
                      <CFormInput
                        type="password"
                        value={password}
                        placeholder="password"
                        onChange={(e) => setPassword(e.target.value)}
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs={6}>
                        <CButton onClick={handleLogin} color="primary" className="px-4">
                          {value.loginbutton}
                        </CButton>
                      </CCol>
                      <CCol xs={6} className="text-right">
                        <CButton color="link" className="px-0">
                          
                        </CButton>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
              <CCard className="text-white bg-primary py-5" style={{ width: '44%' }}>
                <CCardBody className="text-center">
                  <div>
                    <h2>{value.register}</h2>
                    <p>
                    {value.logintext}
                    </p>
                    <div>
                      <h1>Your IP Address is: {ipAddress}</h1>
                    </div>
                    <Link to="/register">
                      <CButton color="primary" className="mt-3" active tabIndex={-1}>
                        {value.registerbutton}
                      </CButton>
                    </Link>
                  </div>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Login
