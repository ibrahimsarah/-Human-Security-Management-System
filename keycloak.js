import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'http://localhost:8080/',
  realm: 'university-realm',
  clientId: 'frontend-client'  
});

export default keycloak;