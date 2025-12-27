import React, { useEffect, useState, useRef } from 'react';  // Add useRef
import keycloak from './keycloak';
import axios from 'axios';
import './App.css';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [students, setStudents] = useState([]);
  const [userInfo, setUserInfo] = useState(null);
  const didInit = useRef(false);  // New ref to track init

useEffect(() => {
  console.log('🚀 Initializing Keycloak...');

  keycloak.init({
    url: 'http://localhost:8080',           // أحيانًا بيحتاجها صريحة لو فيه مشكلة discovery
    realm: 'university-realm',
    clientId: 'frontend-client',
    onLoad: 'login-required',
    flow: 'standard',                       // مهم جدًا للـ Authorization Code Flow
    pkceMethod: 'S256',
    checkLoginIframe: false,
    // أهم حاجة هنا:
    redirectUri: 'http://localhost:3000',   // صريح جدًا، بدون / في الآخر
  })
  .success((authenticated) => {
    console.log('✅ Keycloak init SUCCESS - Authenticated:', authenticated);
    setAuthenticated(authenticated);
    setLoading(false);

    if (authenticated) {
      keycloak.loadUserInfo().then((info) => {
        setUserInfo(info);
      });

      // Token refresh كل 30 ثانية
      setInterval(() => {
        keycloak.updateToken(30).success((refreshed) => {
          if (refreshed) console.log('Token refreshed');
        });
      }, 30000);
    }
  })
  .error((error) => {
    console.error('❌ Keycloak init FAILED:', error);
    setLoading(false);
  });
}, []); 
  // Rest of your code (fetchStudents, addStudent, JSX) remains the same
}

export default App;