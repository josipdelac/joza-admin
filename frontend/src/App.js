import React, { Component, Suspense, useState, useEffect } from 'react'
import { HashRouter, Route, Routes, useHistory, Navigate, redirect } from 'react-router-dom'
import './scss/style.scss'
import localization from './assets/languages/localization.json'

import { LanguageProvider } from './components/localizationContext'
import { get } from 'lodash'
import { UserProvider } from './components/userContext'
import { useGetCurrentUser } from './api/api'
import { element } from 'prop-types'
const loading = (
  <div className="pt-3 text-center">
    <div className="sk-spinner sk-spinner-pulse"></div>
  </div>
)

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Tablica = React.lazy(() => import('./views/pages/login/Tablica'))
const Register = React.lazy(() => import('./views/pages/register/Register'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))
const Users = React.lazy(() => import('./views/pages/login/Users'))
const Edit = React.lazy(() => import('./views/pages/login/Edit'))
const Contacts = React.lazy(() => import('./views/dashboard/Contacts'))
const Logs = React.lazy(() => import('./views/dashboard/Logs'))

const App = () => {
  const [lang, setlang] = useState(localStorage["lang"] || "en")
  const [user, setuser] = useState({ firstname: '', lastname: ''})
  console.log('THereee:::')

  // const navigate= useHistory();

  if (!localStorage.getItem('token')) {
    console.log('Hereee:::')
    localStorage.setItem('token', '');
    if(window.location.pathname !== '/login' || window.location.pathname !== '/redirect'){
      redirect("/login");
    }
    // navigate.replace('/login');
  }


  useEffect(() => {
    const getUser = async () => { 
      const result = await useGetCurrentUser();
     
       return result;
       }

       const fetchData = async () => {
        const response = await getUser();
        setuser(response.data);

      };
    if(localStorage.getItem('token')){
      fetchData();
    } 
  }, [])
  // Clean up interval on component unmount
  const isAuthenticated = localStorage.getItem('token');
  console.log("user", user)
  return (
    <HashRouter>
      <UserProvider value={user}>
        <LanguageProvider value={get(localization, lang)}>
          <Suspense fallback={loading}>
            
            <div style={{ display: 'flex', flexDirection: 'row-reverse' }}>
              <button onClick={() => {setlang('en'); localStorage.setItem('lang', 'en')}}>en</button>
              <button style={{ marginRight: '10px' }}  onClick={() => {setlang('hr'); localStorage.setItem('lang', 'hr')}}>hr</button>
            </div>
            
            <Routes>
              <Route exact path="/login" name="Login Page" element={<Login setUser={setuser} />} />
              <Route
                exact
                path="/register"
                name="Register Page"
                element={<Register setUser={setuser} />}
              />
              <Route exact path="/tablica" name="Tablica" element={<Tablica />} />
              
              <Route exact path="/404" name="Page 404" element={<Page404 />} />
              <Route exact path="/500" name="Page 500" element={<Page500 />} />
              <Route exact path="/users" name="Users"  element={isAuthenticated ? <Users /> : <Navigate to="/login" replace />} />
              <Route exact path="/edit/:id/edit" name="Edit User" element={<Edit />} />
              <Route exact path="/contacts" name="Contacts" element={<Contacts />} />
              <Route exact path="/logs" name="Logs" element={<Logs />} />

              <Route path="*" name="Home" element={<DefaultLayout />} />
            </Routes>
            
          </Suspense>
        </LanguageProvider>
      </UserProvider>
    </HashRouter>
    
  )
}

export default App
