import React, { Component, Suspense, useState } from 'react'
import { HashRouter, Route, Routes } from 'react-router-dom'
import './scss/style.scss'
import localization from './assets/languages/localization.json'
import Select from 'react-select'
import { LanguageProvider } from './components/localizationContext'
import { get } from 'lodash'
import { UserProvider } from './components/userContext'
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
const Kriptiranje = React.lazy(() => import('./views/pages/login/Kriptiranje'))
const Edit = React.lazy(() => import('./views/pages/login/Edit'))

const App = () => {
  const [lang, setlang] = useState('en')
  const [user, setuser] = useState({ firstname: '', lastname: '', picture: '' })
  console.log('THereee:::')

  if (!localStorage.getItem('token')) {
    console.log('Hereee:::')
    localStorage.setItem('token', 'None')
  }
  return (
    <HashRouter>
      <UserProvider value={user}>
        <LanguageProvider value={get(localization, lang)}>
          <Suspense fallback={loading}>
            <div style={{ display: 'flex', flexDirection: 'row-reverse' }}>
              <button onClick={() => setlang('en')}>en</button>
              <button onClick={() => setlang('hr')}>hr</button>
            </div>
            <Routes>
              <Route exact path="/login" name="Login Page" element={<Login setUser={setuser} />} />
              <Route exact path="/tablica" name="Tablica" element={<Tablica />} />
              <Route
                exact
                path="/register"
                name="Register Page"
                element={<Register setUser={setuser} />}
              />
              <Route exact path="/404" name="Page 404" element={<Page404 />} />
              <Route exact path="/500" name="Page 500" element={<Page500 />} />
              <Route exact path="/kriptiranje" name="Kriptiranje" element={<Kriptiranje />} />
              <Route exact path="/edit/:id/edit" name="Edit User" element={<Edit />} />

              <Route path="*" name="Home" element={<DefaultLayout />} />
            </Routes>
          </Suspense>
        </LanguageProvider>
      </UserProvider>
    </HashRouter>
  )
}

export default App
