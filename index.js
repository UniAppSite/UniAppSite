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

// Function to check if user is logged in and redirect if they are
function checkLoggedInRedirect() {
    console.log("Checking if user is logged in...");
    
    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is logged in, redirect to dashboard
            console.log("User is logged in, redirecting to dashboard:", user.email);
            window.location.href = "Services.html";
        } else {
            // User is not logged in, do nothing
            console.log("User is not logged in, staying on current page");
        }
    });
}

// Initialize check when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, checking login state for redirection");
    checkLoggedInRedirect();
});