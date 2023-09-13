import React, { useEffect, useState, useContext } from "react";
import axios from "axios" //npm install axios --save 
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
import { fetchDataRobots } from 'src/api/api';
import LanguageContext from 'src/components/localizationContext'


export default function ListUserPage(){
  
    const [robots, setRobots] = useState([]);
    const value = useContext(LanguageContext);  






    useEffect(() => {
        const getResults = async (id) => { 
          const results = await fetchDataRobots()
            setRobots(results.data)
         
           return results }
    
        getResults();
    
        
      
    
      }, [])
 
      const deleteRobot = (id) => {
        axios.delete(`http://localhost:5000/api/robotdelete/${id}`).then(function(response){
            console.log(response.data);
            setRobots();
        });
        alert("Successfully Deleted");
    }
     
   
    return (
    <div>
        <AppHeader />
        <div className="container h-100">
            <div className="row h-100">
                <div className="col-12">
                    
                    <h1>{value.listrobots}</h1>
                    <table className="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>{value.robotname}</th>
                                <th>{value.status}</th>
                                <th>{value.developby}</th>
                                <th>{value.department}</th>
                                <th>{value.actions}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {robots.map((robots, key) =>
                                <tr key={key}>
                                    <td>{key + 1}</td>
                                    <td>{robots.robot_name}</td>
                                    <td>{robots.robot_status}</td>
                                    <td>{robots.developby}</td>
                                    <td>{robots.organization_name}</td>
                                    <td>
                                    <button onClick={() => deleteRobot(robots.id)} className="btn btn-danger">{value.delete}</button></td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
  );
}