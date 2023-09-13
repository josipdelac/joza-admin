import React, { useState, useEffect, useContext } from 'react'
import { PDFViewer } from '@react-pdf/renderer'
import TableReport from './TableReport'
import utf8 from 'utf8';

import Modal from 'react-modal';
import {
  CAvatar,
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol,
  CProgress,
  CRow,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
} from '@coreui/react'
import { CChartLine } from '@coreui/react-chartjs'
import { getStyle, hexToRgba } from '@coreui/utils'
import CIcon from '@coreui/icons-react'
import {
  cibCcAmex,
  cibCcApplePay,
  cibCcMastercard,
  cibCcPaypal,
  cibCcStripe,
  cibCcVisa,
  cibGoogle,
  cibFacebook,
  cibLinkedin,
  cifBr,
  cifEs,
  cifFr,
  cifIn,
  cifPl,
  cifUs,
  cibTwitter,
  cilCloudDownload,
  cilPeople,
  cilUser,
  cilUserFemale,
  moment,
} from '@coreui/icons'


import WidgetsDropdown from '../widgets/WidgetsDropdown'
import { useGetRobotStatus, useGetRobotStatusLastEntry, useGetRobotsStatusLastEntries, useGetProcessedItems } from 'src/api/api'
import { jsPDF } from "jspdf";
import jsRTF from 'jsrtf';
import { saveAs } from 'file-saver';
import LanguageContext from 'src/components/localizationContext'
import {useNavigate } from 'react-router-dom';
import iconv from 'iconv-lite';
const Dashboard = () => {
  const random = (min, max) => Math.floor(Math.random() * (max - min + 1) + min)

  const progressExample = [
    { title: 'Visits', value: '29.703 Users', percent: 40, color: 'success' },
    { title: 'Unique', value: '24.093 Users', percent: 20, color: 'info' },
    { title: 'Pageviews', value: '78.706 Views', percent: 60, color: 'warning' },
    { title: 'New Users', value: '22.123 Users', percent: 80, color: 'danger' },
    { title: 'Bounce Rate', value: 'Average Rate', percent: 40.15, color: 'primary' },
  ]
  const [robotEntries, setRobotEntries] = useState([])
  const [last_entry, setlast_entry] = useState([])
  const [showPDF, setShowPDF] = useState(false);
  const [visible, setVisible] = useState(false)
  

  const [total_processed, setTotalProcessed] = useState({pdf: 0, web:0, K:0})
  const value = useContext(LanguageContext);  
  console.log("Context", value)
  const generatePDF = () => {
    setShowPDF(true);
  };
  useEffect(() => {
    const getResults = async (id) => { 
      const results = await Promise.all( [useGetRobotsStatusLastEntries(),  useGetRobotStatusLastEntry(id),useGetProcessedItems("pdf"),useGetProcessedItems("web"), useGetProcessedItems("K")]);
      
     
       return results }

    /*const result = getResults("ROO").then((response) => {
      setRobotEntries(response[0].data)
      setlast_entry([response[1].data])
    });*/
    const fetchData = async () => {
      const response = await getResults();
      console.log("lastdsadsada:",response[1])
      setRobotEntries(response[0].data);
      console.log("setRobotEntries",response[0].data)
      setlast_entry([response[1]]);
      console.log("setlast_entry",response[1])
      setTotalProcessed({pdf: response[2].data, web:response[3].data, K:response[4].data, total:response[2].data+response[3].data+response[4].data})
      
    };

    fetchData();
    const intervalId = setInterval(fetchData, 100000000);

  // Clean up interval on component unmount
  return () => {
    clearInterval(intervalId);
  };

    
  

  }, [])

  const currentDate = new Date().toLocaleDateString();



  const generateRTF = (robotEntries) => {
    let rtfContent = `{\rtf1
  {\fonttbl{\f0 Times New Roman;}}
  {\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red0\green255\blue0;}
  {\pard\cf1\qc\fs24 Report Title\par}
  {\pard\qc\fs20\cf0
  \\trowd\\cellx1440\\cellx2880\\cellx4320\\cellx5760\\cellx7200
  \\cf2 Robot Name\\cell Status\\cell Progress\\cell Server\\cell Last Updated\\row
  }`;
  
    robotEntries.forEach((item) => {
      // Encode special characters using iconv-lite
      const name = iconv.encode(item.name, 'win1252').toString('binary');
      const status = iconv.encode(item.status, 'win1252').toString('binary');
      const serverId = iconv.encode(item.server_id, 'win1252').toString('binary');
      const row = `\\trowd\\cellx1440\\cellx2880\\cellx4320\\cellx5760\\cellx7200
  \\pard\\qc ${name}\\cell ${status}\\cell ${item.current_item}/${item.total_items}\\cell ${serverId}\\cell ${item.datum}\\row`;
      rtfContent += row;
    });
  
    rtfContent += '}';
  
    // Create a Blob and save it as an RTF file
    const blob = new Blob([rtfContent], { type: 'application/rtf' });
    saveAs(blob, 'report.rtf');
  };
  
   const localization= useContext('lo')

  

  return (
    <>
      <WidgetsDropdown />
      
      {/* <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol sm={5}>
              <h4 id="traffic" className="card-title mb-0">
                Traffic
              </h4>
              <div className="small text-medium-emphasis">January - July 2021</div>
            </CCol>
            <CCol sm={7} className="d-none d-md-block">
              <CButton color="primary" className="float-end">
                <CIcon icon={cilCloudDownload} />
              </CButton>
              <CButtonGroup className="float-end me-3">
                {['Day', 'Month', 'Year'].map((value) => (
                  <CButton
                    color="outline-secondary"
                    key={value}
                    className="mx-0"
                    active={value === 'Month'}
                  >
                    {value}
                  </CButton>
                ))}
              </CButtonGroup>
            </CCol>
          </CRow>
          <CChartLine
            style={{ height: '300px', marginTop: '40px' }}
            data={{
              labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
              datasets: [
                {
                  label: 'My First dataset',
                  backgroundColor: hexToRgba(getStyle('--cui-info'), 10),
                  borderColor: getStyle('--cui-info'),
                  pointHoverBackgroundColor: getStyle('--cui-info'),
                  borderWidth: 2,
                  data: [
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                  ],
                  fill: true,
                },
                {
                  label: 'My Second dataset',
                  backgroundColor: 'transparent',
                  borderColor: getStyle('--cui-success'),
                  pointHoverBackgroundColor: getStyle('--cui-success'),
                  borderWidth: 2,
                  data: [
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                    random(50, 200),
                  ],
                },
                {
                  label: 'My Third dataset',
                  backgroundColor: 'transparent',
                  borderColor: getStyle('--cui-danger'),
                  pointHoverBackgroundColor: getStyle('--cui-danger'),
                  borderWidth: 1,
                  borderDash: [8, 5],
                  data: [65, 65, 65, 65, 65, 65, 65],
                },
              ],
            }}
            options={{
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    drawOnChartArea: false,
                  },
                },
                y: {
                  ticks: {
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    stepSize: Math.ceil(250 / 5),
                    max: 250,
                  },
                },
              },
              elements: {
                line: {
                  tension: 0.4,
                },
                point: {
                  radius: 0,
                  hitRadius: 10,
                  hoverRadius: 4,
                  hoverBorderWidth: 3,
                },
              },
            }}
          />
        </CCardBody>
        <CCardFooter>
          <CRow xs={{ cols: 1 }} md={{ cols: 5 }} className="text-center">
            {progressExample.map((item, index) => (
              <CCol className="mb-sm-2 mb-0" key={index}>
                <div className="text-medium-emphasis">{item.title}</div>
                <strong>
                  {item.value} ({item.percent}%)
                </strong>
                <CProgress thin className="mt-2" color={item.color} value={item.percent} />
              </CCol>
            ))}
          </CRow>
        </CCardFooter>
      </CCard> */} 


      <CRow>
        <CCol xs>
          <CCard className="mb-4">
            <CCardHeader>{value.totalstatistics}</CCardHeader>
            <CCardBody>
              <CRow>
                <CCol xs={12} md={6} xl={6}>
                  <CRow>
                    <CCol sm={6}>
                      <div className="border-start border-start-4 border-start-info py-1 px-3">
                        <div className="text-medium-emphasis small">{value.documents_processed} </div>
                        <div className="fs-5 fw-semibold">{total_processed.pdf}</div>
                      </div>
                    </CCol>
                    <CCol sm={6}>
                      <div className="border-start border-start-4 border-start-danger py-1 px-3 mb-3">
                        <div className="text-medium-emphasis small">{value.documents_processed_K}</div>
                        <div className="fs-5 fw-semibold">{total_processed.K}</div>
                      </div>
                    </CCol>
                  </CRow>

                  <hr className="mt-0" />
                  {/*progressGroupExample1.map((item, index) => (
                    <div className="progress-group mb-4" key={index}>
                      <div className="progress-group-prepend">
                        <span className="text-medium-emphasis small">{item.title}</span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress thin color="info" value={item.value1} />
                        <CProgress thin color="danger" value={item.value2} />
                      </div>
                    </div>
                  ))*/}
                </CCol>

                <CCol xs={12} md={6} xl={6}>
                  <CRow>
                    <CCol sm={6}>
                      <div className="border-start border-start-4 border-start-warning py-1 px-3 mb-3">
                        <div className="text-medium-emphasis small">{value.documents_processed_web}</div>
                        <div className="fs-5 fw-semibold">{total_processed.web}</div>
                      </div>
                    </CCol>
                    <CCol sm={6}>
                      <div className="border-start border-start-4 border-start-success py-1 px-3 mb-3">
                        <div className="text-medium-emphasis small">{value.total}</div>
                        <div className="fs-5 fw-semibold">{total_processed.total}</div>
                      </div>
                    </CCol>
                  </CRow>

                  <hr className="mt-0" />

                  {/*progressGroupExample2.map((item, index) => (
                    <div className="progress-group mb-4" key={index}>
                      <div className="progress-group-header">
                        <CIcon className="me-2" icon={item.icon} size="lg" />
                        <span>{item.title}</span>
                        <span className="ms-auto fw-semibold">{item.value}%</span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress thin color="warning" value={item.value} />
                      </div>
                    </div>
                  ))*/}

                  <div className="mb-5"></div>

                  {/* {progressGroupExample3.map((item, index) => (
                    <div className="progress-group" key={index}>
                      <div className="progress-group-header">
                        <CIcon className="me-2" icon={item.icon} size="lg" />
                        <span>{item.title}</span>
                        <span className="ms-auto fw-semibold">
                          {item.value}{' '}
                          <span className="text-medium-emphasis small">({item.percent}%)</span>
                        </span>
                      </div>
                      <div className="progress-group-bars">
                        <CProgress thin color="success" value={item.percent} />
                      </div>
                    </div>
                  ))} */}
                </CCol>
              </CRow>

              <br />

              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableHead color="light">
                  <CTableRow>
                    <CTableHeaderCell className="text-center">
                      <CIcon icon={cilPeople} />
                    </CTableHeaderCell>
                    <CTableHeaderCell className="text-center">Robot</CTableHeaderCell>
                    <CTableHeaderCell className="text-center">Satus</CTableHeaderCell>
                    <CTableHeaderCell className="text-center">{value.progress}</CTableHeaderCell>
                    <CTableHeaderCell className="text-center">Server</CTableHeaderCell>
                    {/* <CTableHeaderCell className="text-center">Payment Method</CTableHeaderCell> */}
                    <CTableHeaderCell className="text-center">{value.lastupdate}</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {robotEntries.map((item, index) => (
                    <CTableRow v-for="item in tableItems" key={index}>
                
                                           
                      <CTableDataCell>
                       
                       <CProgress  thin color="blue" value={item.current_item*1} />
                      </CTableDataCell>
                      {/* <CTableDataCell className="text-center">
                        <CIcon size="xl" icon={item.payment.icon} />
                      </CTableDataCell> */}
                      <CTableDataCell className="text-center">
                        
                        <strong >{item.name}</strong>
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                        
                        <strong>{item.status}</strong>
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                        {/* <div className="small text-medium-emphasis">Last login</div> */}
                        
                        <strong>{item.current_item+"/"+item.total_items}</strong>
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                        
                        <strong>{item.server_id}</strong>
                      </CTableDataCell>
                      <CTableDataCell className="text-center">
                                            
                        <strong>{item.datum}</strong>
                      </CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
              <br/>
        
              <CButton style={{ marginRight: '10px' }} onClick={() => setVisible(!visible)}>PDF</CButton>
              <CModal visible={visible} onClose={() => setVisible(false)} style={{ width: '850px', height: '700px' }}>
                <CModalHeader onClose={() => setVisible(false)}>
                  <CModalTitle>Robot's Report</CModalTitle>
                </CModalHeader>
                <CModalBody>
                  <PDFViewer width="800" height="600">
                      <TableReport robotEntries={robotEntries} />
                  </PDFViewer>
                </CModalBody>
                <CModalFooter>
                  <CButton color="primary" onClick={() => setVisible(false)}>
                    Close
                  </CButton>
                  
                </CModalFooter>
              </CModal>
             
              <CButton  onClick= {() => generateRTF(robotEntries)}>RTF</CButton>

            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Dashboard
