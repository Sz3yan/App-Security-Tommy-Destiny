import { initializeApp } from 'firebase/app';

require('dotenv').config();

const firebaseConfig = {
    apiKey: process.env.API_KEY,
    authDomain: process.env.AUTH_DOMAIN,
    databaseURL: process.env.DATABASE_URL,
    projectId: process.env.PROJ_ID,
    storageBucket: process.env.S_BUCKET,
    messagingSenderId: process.env.M_SENDER_ID,
    appId: process.env.APP_ID,
    measurementId: process.env.M_ID
};
  
const app = initializeApp(firebaseConfig);

