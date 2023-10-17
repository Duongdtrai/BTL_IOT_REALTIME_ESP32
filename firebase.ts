// npm install firebase
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCAx3QAAZCVzX4Swg7TluMLsZEgbNpSUb0",
  authDomain: "esp32-temperature-real-time.firebaseapp.com",
  projectId: "esp32-temperature-real-time",
  storageBucket: "esp32-temperature-real-time.appspot.com",
  messagingSenderId: "92656498925",
  appId: "1:92656498925:web:b0eda228582b527d2734e4",
  measurementId: "G-J8BF5D6GN5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);