// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA4NwuYpaWbJq22FH2oxG3q4XdNsDH62b0",
    authDomain: "uniapp-20192.firebaseapp.com",
    projectId: "uniapp-20192",
    storageBucket: "uniapp-20192.firebasestorage.app",
    messagingSenderId: "313585313532",
    appId: "1:313585313532:web:7e0ab65ee1c485f171d979",
    measurementId: "G-E6YH32BM9Q"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Function to check authentication and handle user state
function checkAuthState() {
    // Access onAuthStateChanged from the imported module
    onAuthStateChanged(auth, (user) => {
        if (!user) {
            // User is not logged in, redirect to login page
            console.log("No user found, redirecting to login page");
            window.location.href = "login.html";
        } else {
            // User is logged in, update welcome message
            console.log("User logged in:", user.email);
            const welcomeMessage = document.getElementById("welcome-message");
            if (welcomeMessage) {
                welcomeMessage.innerText = `Welcome, Logged In as ${user.email}`;
            }
        }
    });
}

// Initialize authentication check when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, checking auth state");
    checkAuthState();
});