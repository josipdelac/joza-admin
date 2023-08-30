/* import React, { useState } from 'react';
import axios from 'axios';
import { CAlert } from '@coreui/react'



function App() {
  const [excelIzlaznaPutanja, setExcelIzlaznaPutanja] = useState('');
  const [pdfDirektorijum, setPdfDirektorijum] = useState('');

  const handleRunProcess = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/tablice', {
        excel_izlazna_putanja: excelIzlaznaPutanja,
        pdf_direktorijum: pdfDirektorijum
      });

      alert(response.data.message);
      console.log(response.data.message);
      setVisible(true)
    } catch (error) {
      console.error(error.response ? error.response.data.error : error.message);
    }
  };

  const [visible, setVisible] = useState(false)


  return (
    <div className="App">
    <CAlert color="primary" dismissible visible={visible} onClose={() => setVisible(false)}>
      TEst
    </CAlert>
      <input
        type="text"
        placeholder="Excel Izlazna Putanja"
        value={excelIzlaznaPutanja}
        onChange={e => setExcelIzlaznaPutanja(e.target.value)}
      />
      <input
        type="text"
        placeholder="PDF Direktorijum"
        value={pdfDirektorijum}
        onChange={e => setPdfDirektorijum(e.target.value)}
      />
      <button onClick={handleRunProcess}>Pokreni Proces B</button>
    </div>
  );
}

export default App;
*/
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
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilMagnifyingGlass } from '@coreui/icons'

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
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={6}>
          <CAlert color="primary" dismissible visible={visible} onClose={() => setVisible(false)}>
          {message}
            
          </CAlert>
            <div className="clearfix">
            <input
            type="text"
            placeholder="Excel Izlazna Putanja"
            value={excelIzlaznaPutanja}
            onChange={e => setExcelIzlaznaPutanja(e.target.value)}
            />
            <input
            type="text"
            placeholder="PDF Direktorijum"
            value={pdfDirektorijum}
            onChange={e => setPdfDirektorijum(e.target.value)}
            />
        <button onClick={handleRunProcess}>Pokreni Proces B</button>
            </div>
            <CInputGroup className="input-prepend">
              <CInputGroupText>
                <CIcon icon={cilMagnifyingGlass} />
              </CInputGroupText>
              <CFormInput type="text" placeholder="What are you looking for?" />
              <CButton color="info">Search</CButton>
            </CInputGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default App
