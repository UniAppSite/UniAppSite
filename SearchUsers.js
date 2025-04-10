// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-auth.js";
import { getFirestore, collection, getDocs, query, where, orderBy, limit, doc, getDoc } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-firestore.js";

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
const auth = getAuth();
const db = getFirestore();

let currentUser = null;
let currentUserData = null;

// Check if user is logged in
onAuthStateChanged(auth, async (user) => {
    if (user) {
        currentUser = user;
        await loadCurrentUserData();
        loadAllUsers(); // Load users on page load
    } else {
        console.log("No user logged in");
        window.location.href = "index.html"; // Redirect to login page
    }
});

// Load current user data for the top-left shortcut
async function loadCurrentUserData() {
    try {
        // Get document directly using the user's UID
        const docRef = doc(db, "users", currentUser.uid);
        const docSnap = await getDoc(docRef);
        
        if (docSnap.exists()) {
            currentUserData = docSnap.data();
            
            // Update the user shortcut
            const currentUserPic = document.querySelector(".current-user-pic");
            const currentUserImage = currentUserPic.querySelector("img");
            const currentUserName = document.getElementById("currentUserName");
            
            if (currentUserData.profilePicture && currentUserImage) {
                currentUserImage.src = currentUserData.profilePicture;
                currentUserImage.style.display = 'block';
            } else if (currentUserImage) {
                // Set a default avatar if no profile picture
                currentUserImage.src = "default-avatar.png"; // Default image path
                currentUserImage.style.display = 'block';
            }
            
            if (currentUserName) {
                currentUserName.innerText = currentUserData.firstName || "User";
            }
            
            // Add click event to redirect to profile
            const userShortcut = document.getElementById("currentUserShortcut");
            if (userShortcut) {
                userShortcut.addEventListener("click", () => {
                    window.location.href = "Profile.html";
                });
            }
        } else {
            console.log("No user document found!");
        }
    } catch (error) {
        console.error("Error loading current user data:", error);
    }
}

// DOM Content loaded event
document.addEventListener("DOMContentLoaded", () => {
    // Button to go back to profile
    const backButton = document.getElementById("backToProfile");
    if (backButton) {
        backButton.addEventListener("click", () => {
            window.location.href = "Profile.html";
        });
    }

    // Search functionality
    const searchBtn = document.getElementById("searchBtn");
    if (searchBtn) {
        searchBtn.addEventListener("click", () => {
            const searchTerm = document.getElementById("searchInput").value.trim();
            searchUsers(searchTerm);
        });
    }

    // Also trigger search on Enter key
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("keyup", (event) => {
            if (event.key === "Enter") {
                const searchTerm = document.getElementById("searchInput").value.trim();
                searchUsers(searchTerm);
            }
        });
    }
});

// Load all users from Firestore
async function loadAllUsers() {
    showLoader(true);
    try {
        const usersCollection = collection(db, "users");
        const q = query(usersCollection, orderBy("firstName"), limit(50));
        const querySnapshot = await getDocs(q);
        
        displayUsers(querySnapshot);
    } catch (error) {
        console.error("Error loading users: ", error);
        showError("Failed to load users. Please try again.");
    } finally {
        showLoader(false);
    }
}

// Search users based on input - now includes first name, last name, and email
async function searchUsers(searchTerm) {
    showLoader(true);
    try {
        if (!searchTerm) {
            loadAllUsers();
            return;
        }

        const usersCollection = collection(db, "users");
        const searchTermLower = searchTerm.toLowerCase();
        
        // Get all users since Firestore doesn't support OR conditions across fields
        const querySnapshot = await getDocs(usersCollection);
        
        // Filter users client-side for more flexible searching
        const filteredResults = [];
        
        querySnapshot.forEach(doc => {
            const userData = doc.data();
            
            // Skip current user
            if (currentUser && doc.id === currentUser.uid) return;
            
            const firstName = (userData.firstName || "").toLowerCase();
            const lastName = (userData.lastName || "").toLowerCase();
            const email = (userData.email || "").toLowerCase();
            
            // Check if any field includes the search term
            if (firstName.includes(searchTermLower) || 
                lastName.includes(searchTermLower) || 
                email.includes(searchTermLower)) {
                filteredResults.push({ id: doc.id, data: userData });
            }
        });
        
        displayFilteredUsers(filteredResults);
        
    } catch (error) {
        console.error("Error searching users: ", error);
        showError("Failed to search users. Please try again.");
    } finally {
        showLoader(false);
    }
}

// Display filtered users
function displayFilteredUsers(filteredUsers) {
    const usersList = document.getElementById("usersList");
    const noResults = document.getElementById("noResults");
    
    if (!usersList || !noResults) return;
    
    usersList.innerHTML = "";
    
    if (filteredUsers.length === 0) {
        noResults.style.display = "block";
        return;
    }
    
    noResults.style.display = "none";
    
    filteredUsers.forEach(user => {
        const userCard = createUserCard(user.id, user.data);
        usersList.appendChild(userCard);
    });
}

// Display users in the UI
function displayUsers(querySnapshot) {
    const usersList = document.getElementById("usersList");
    const noResults = document.getElementById("noResults");
    
    if (!usersList || !noResults) return;
    
    usersList.innerHTML = "";
    
    if (querySnapshot.empty) {
        noResults.style.display = "block";
        return;
    }
    
    noResults.style.display = "none";
    
    querySnapshot.forEach((doc) => {
        const userData = doc.data();
        // Don't show current user in the list
        if (currentUser && doc.id === currentUser.uid) return;
        
        const userCard = createUserCard(doc.id, userData);
        usersList.appendChild(userCard);
    });
}

// Create user card element
function createUserCard(userId, userData) {
    const userCard = document.createElement("div");
    userCard.className = "user-card";
    userCard.dataset.userId = userId;
    
    const defaultProfilePic = ""; // Add a default placeholder if needed
    const profilePic = userData.profilePicture || defaultProfilePic;
    const firstName = userData.firstName || "Unknown";
    const lastName = userData.lastName || "";
    const fullName = lastName ? `${firstName} ${lastName}` : firstName;
    const aboutMe = userData.aboutMe || "Hello, I'm New Here";
    
    userCard.innerHTML = `
        <div class="user-pic">
            <img src="${profilePic}" alt="${fullName}" onerror="this.style.display='none';">
        </div>
        <div class="user-name">${fullName}</div>
        <div class="user-about">${aboutMe}</div>
    `;
    
    // Add click event to open user details modal
    userCard.addEventListener("click", () => {
        openUserModal(userData);
    });
    
    return userCard;
}

// Open user details modal
function openUserModal(userData) {
    const modal = document.getElementById("userDetailsModal");
    const modalUserImage = document.getElementById("modalUserImage");
    const modalUserName = document.getElementById("modalUserName");
    const modalUserEmail = document.getElementById("modalUserEmail");
    const modalAboutMe = document.getElementById("modalAboutMe");
    
    if (!modal || !modalUserName || !modalUserEmail || !modalAboutMe) return;
    
    // Populate modal with user data
    if (modalUserImage) {
        modalUserImage.src = userData.profilePicture || "";
        modalUserImage.onerror = function() { this.style.display = 'none'; };
        modalUserImage.onload = function() { this.style.display = 'block'; };
    }
    
    const firstName = userData.firstName || "Unknown";
    const lastName = userData.lastName || "";
    const fullName = lastName ? `${firstName} ${lastName}` : firstName;
    
    modalUserName.innerText = fullName;
    modalUserEmail.innerText = userData.email || "No email provided";
    modalAboutMe.innerText = userData.aboutMe || "Hello, I'm New Here";
    
    modal.style.display = "flex";
}

// Close user details modal
window.closeUserModal = function() {
    const modal = document.getElementById("userDetailsModal");
    if (modal) {
        modal.style.display = "none";
    }
};

// Helper functions
function showLoader(show) {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = show ? "block" : "none";
    }
}

function showError(message) {
    const noResults = document.getElementById("noResults");
    if (noResults) {
        noResults.innerHTML = `<p>${message}</p>`;
        noResults.style.display = "block";
    }
}

// Close the modal if user clicks outside of it
window.addEventListener("click", (event) => {
    const modal = document.getElementById("userDetailsModal");
    if (modal && event.target === modal) {
        closeUserModal();
    }
});