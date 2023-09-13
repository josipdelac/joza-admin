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


export default function ListUserPage(){
  
    const [users, setUsers] = useState([]);





    useEffect(() => {
        const getResults = async (id) => { 
          const results = await fetchData()
            setUsers(results.data)
         
           return results }
    
        getResults();
    
        
      
    
      }, [])
 

     
    const deleteUser = (id) => {
        axios.delete(`http://localhost:5000/api/userdelete/${id}`).then(function(response){
            console.log(response.data);
            getUsers();
        });
        alert("Successfully Deleted");
    }
     
    return (
    <div>
        <AppHeader />
        <div className="container h-100">
            <div className="row h-100">
                <div className="col-12">
                    
                    <h1>List Users</h1>
                    <table className="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Email</th>
                                <th>Country</th>
                                <th>Actions</th>
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
                                    <td>
                                        <Link to={`/edit/${user.id}/edit`} className="btn btn-success" style={{marginRight: "10px"}}>Edit</Link>
                                        <button onClick={() => deleteUser(user.id)} className="btn btn-danger">Delete</button>
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