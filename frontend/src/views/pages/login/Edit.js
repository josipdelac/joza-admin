import React, { useState, useEffect  } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
 
export default function EditUser(){
  
    const navigate = useNavigate();
  
    const [inputs, setInputs] = useState({
        first_name: '',
        last_name: '',
        email: '',
        country: '',
    });
  
    const {id} = useParams();
  
    useEffect(() => {
        getUser();
    }, []);
  
    function getUser() {
        axios.get(`http://localhost:5000/api/userdetails/${id}/edit`).then(function(response) {
            console.log(response.data);
            setInputs(response.data);
        });
    }
  
    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}));
    }
    const handleSubmit = (event) => {
        event.preventDefault();
  
        axios.put(`http://localhost:5000/api/userupdate/${id}/edit`, inputs).then(function(response){
            console.log(response.data);
            navigate('/kriptiranje');
        });
          
    }
     
    return (
    <div>
        <div className="container h-100">
        <div className="row">
            <div className="col-2"></div>
            <div className="col-8">
            <h1>Edit user</h1>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label>First Name</label>
                  <input type="text" value={inputs.first_name} className="form-control" name="first_name" onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label>Last Name</label>
                  <input type="text" value={inputs.last_name} className="form-control" name="last_name" onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label>Email</label>
                  <input type="text" value={inputs.email} className="form-control" name="email" onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label>Country</label>
                  <input type="text" value={inputs.country} className="form-control" name="country" onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label>Type of user</label>
                  <input type="text" value={inputs.type} className="form-control" name="country" onChange={handleChange} />
                </div>        
                <button type="submit" name="update" className="btn btn-primary">Save</button>
            </form>
            </div>
            <div className="col-2"></div>
        </div>
        </div>
    </div>
  );
}