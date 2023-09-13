;<script
  defer
  src="https://polyfill.io/v3/polyfill.min.js?features=String.prototype.padEnd|always"
></script>
import React, { useState, useEffect,useContext } from 'react'
import { Link } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CFormSelect,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser } from '@coreui/icons'
import axios from 'axios'
import { convert } from 'xml2js' // xml2js library for converting XML to JSON
import { useNavigate } from 'react-router-dom'
import LanguageContext from 'src/components/localizationContext'


const Register = (props) => {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [country, setCountry] = useState('')
  const [countryOptions, setCountryOptions] = useState([])
  const [profileImage, setProfileImage] = useState(null)
  const navigate = useNavigate()
  const { setUser } = props
  const value = useContext(LanguageContext);  
  



  const handleImageChange = (e) => {
    const imageFile = e.target.files[0]
    const reader = new FileReader()

    reader.onload = (event) => {
      const base64Image = event.target.result.split(',')[1]
      setProfileImage(base64Image)
    }

    reader.readAsDataURL(imageFile)
  }

  useEffect(() => {
    const fetchCountryNames = async () => {
      const soapRequest = `
        <soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
          <soap12:Body>
            <ListOfCountryNamesByName xmlns="http://www.oorsprong.org/websamples.countryinfo">
            </ListOfCountryNamesByName>
          </soap12:Body>
        </soap12:Envelope>
      `

      try {
        const response = await axios.post('http://localhost:5000/api/countries', soapRequest, {
          headers: {
            'Content-Type': 'application/soap+xml;charset=UTF-8',
            'Accept-Encoding': 'gzip,deflate',
          },
        })
        console.log(response)

        setCountryOptions(response?.data)
      } catch (error) {
        console.error('Error fetching country names:', error)
      }
    }

    fetchCountryNames()
  }, [])

  const handleRegister = async () => {
    try {
      const data = {
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        country,
        profile_image: profileImage,
      }

      const response = await axios.post('http://localhost:5000/api/register', data)

      if (response.data.message === 'User registered successfully') {
        alert(response.data.message)
        localStorage.setItem('token', response.data.jwt)
        setUser(response.data.user_details)
        navigate('/dashboard') // Preusmjeri korisnika na dashboard nakon prijave
      } else {
        alert(response.data.message)
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }
  const localization= useContext('lo')

  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={9} lg={7} xl={6}>
            <CCard className="mx-4">
              <CCardBody className="p-4">
                <CForm>
                  <h1>{value.registertext}</h1>
                  <p className="text-medium-emphasis">{value.registerparagraf}</p>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilUser} />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="First Name"
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilUser} />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Last Name"
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>@</CInputGroupText>
                    <CFormInput
                      placeholder="Email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-4">
                    <CInputGroupText>🌍</CInputGroupText>
                    <CFormSelect
                      aria-label="Country"
                      value={country}
                      onChange={(e) => setCountry(e.target.value)}
                    >
                      <option style={{ padding: '0.5rem 0rem' }} value="">
                        Odaberi državu
                      </option>
                      {countryOptions?.map((countryName, index) => (
                        <option style={{ padding: '0.5rem 0rem' }} key={index} value={countryName}>
                          {countryName}
                        </option>
                      ))}
                    </CFormSelect>
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    {/* Dodajte input za odabir slike */}
                    <CFormInput type="file" accept="image/*" onChange={handleImageChange} />
                  </CInputGroup>
                  <div className="d-grid">
                    <CButton color="success" onClick={handleRegister}>
                      Create Account
                    </CButton>
                  </div>
                </CForm>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Register
