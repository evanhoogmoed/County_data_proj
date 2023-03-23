import React from 'react';
import ReactDOM from 'react-dom/client';
import SwaggerUI from 'swagger-ui-react';
import "swagger-ui-react/swagger-ui.css"
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
    <SwaggerUI url="http://localhost:5000/swagger" />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
