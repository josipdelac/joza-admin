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
import { fetchData } from 'src/api/api';
import LanguageContext from 'src/components/localizationContext'


export default function ListUserPage(){
  
    const [users, setUsers] = useState([]);
    const value = useContext(LanguageContext); 
    const getResults = async (id) => {
        try {
          const results = await fetchData();
          setUsers(results.data);
          return results
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };





    useEffect(() => {
        
    
        getResults();
    
        
      
    
      }, [])
 

     
    const deleteUser = (id) => {
        axios.delete(`http://localhost:5000/api/userdelete/${id}`).then(function(response){
            console.log(response.data);
            getResults();
        });
        alert("Successfully Deleted");
    }
     
    return (
    <div>
        <AppHeader />
        <div className="container h-100">
            <div className="row h-100">
                <div className="col-12">
                    
                    <h1>{value.listusers}</h1>
                    <table className="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>{value.firstname}</th>
                                <th>{value.lastname}</th>
                                <th>{value.email}</th>
                                <th>{value.country}</th>
                                <th>{value.typeofuser}</th>
                                <th>{value.department}</th>
                                <th>{value.sector}</th>
                                <th>{value.actions}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user, key) =>
                                <tr key={key}>
                                    <td>{key + 1}</td>
                                    <td>{user.first_name}</td>
                                    <td>{user.last_name}</td>
                                    <td>{user.email}</td>
                                    <td>{user.country}</td>
                                    <td>{user.type}</td>
                                    <td>{user.department}</td>
                                    <td>{user.sector}</td>
                                    <td>
                                        <Link to={`/edit/${user.id}/edit`} className="btn btn-success" style={{marginRight: "10px"}}>{value.edit}</Link>
                                        <button onClick={() => deleteUser(user.id)} className="btn btn-danger">{value.delete}</button>
                                    </td>
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