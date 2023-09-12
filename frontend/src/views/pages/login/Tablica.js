import React, { useState } from 'react';
import axios from 'axios';

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


function App() {
    const [excelIzlaznaPutanja, setExcelIzlaznaPutanja] = useState('');
    const [pdfDirektorijum, setPdfDirektorijum] = useState('');
    const [message, setMessage] = useState('');
  
    const handleRunProcess = async () => {
      try {
        const response = await axios.post('http://localhost:5000/api/tablice', {
          excel_izlazna_putanja: excelIzlaznaPutanja,
          pdf_direktorijum: pdfDirektorijum
        });
  
        setMessage(response.data.message);
        
        console.log(response.data.message);
        setVisible(true)
      } catch (error) {
        console.error(error.response ? error.response.data.error : error.message);
      }
    };
  
    const [visible, setVisible] = useState(false)
  return (
    
    <div>
      <AppHeader />
      <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={8}>
          <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm>
                  <h1>HZMO tablice</h1>
                  <p className="text-medium-emphasis">HZMO data extraction from pdf to .xlsx file</p>
                  <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilFile} />
                      </CInputGroupText>
                      <CFormInput type="text" 
                                  value={excelIzlaznaPutanja}  onChange={e => setExcelIzlaznaPutanja(e.target.value)} placeholder="Excel Izlazna Putanja" />
                    </CInputGroup>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilFolderOpen} />
                      </CInputGroupText>
                      <CFormInput type="text" 
                                  value={pdfDirektorijum}  onChange={e => setPdfDirektorijum(e.target.value)} placeholder="PDF direktorij" />
                    </CInputGroup>

                    <CAlert color="primary" dismissible visible={visible} onClose={() => setVisible(false)}>
                    {message}
                      
                    </CAlert>
                    <CRow>
                      <CCol xs={6}>
                        <CButton onClick={handleRunProcess} color="primary" className="px-4 align-items-center">
                          Pokreni proces
                        </CButton>
                      </CCol>
                      
                    </CRow>
                    
                     
                      
                  </CForm>
                </CCardBody>
              </CCard>
            </CCardGroup>
            </CCol>
          </CRow>
        </CContainer>
      </div>
    </div>
    
    
  )
}

export default App
