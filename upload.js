import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";
import { getFirestore, doc, getDoc, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";

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

// ImgBB API key - Replace with your actual API key
const IMGBB_API_KEY = "4f4d9f58466506463ea37dce6f973243";

let userData = {};

// Check if user is logged in
onAuthStateChanged(auth, async (user) => {
    if (user) {
        const userId = user.uid;
        const docRef = doc(db, "users", userId);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
            userData = docSnap.data();
            document.getElementById('loggedUserFName').innerText = userData.firstName || "Unknown";
            document.getElementById('loggedUserEmail').innerText = userData.email || "Unknown";
        } else {
            console.log("User document not found");
            window.location.href = "index.html"; // Redirect to login page
        }
    } else {
        console.log("No user logged in");
        window.location.href = "index.html"; // Redirect to login page
    }
});

// Show file name when selected
document.getElementById("imageFile").addEventListener("change", function() {
    const fileName = this.files[0]?.name || "No file selected";
    document.getElementById("fileName").textContent = fileName;
    
    // Show image preview
    if (this.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const previewContainer = document.getElementById("imagePreview");
            const previewImage = document.getElementById("previewImage");
            
            previewImage.src = e.target.result;
            previewContainer.style.display = "block";
        }
        reader.readAsDataURL(this.files[0]);
    }
});

// Upload image to ImgBB and then store URL in Firebase
document.getElementById("uploadBtn").addEventListener("click", async () => {
    const fileInput = document.getElementById("imageFile");
    const socialUsername = document.getElementById("socialUsername").value.trim();
    const statusMessage = document.getElementById("statusMessage");

    // Validate file selection
    if (!fileInput.files || fileInput.files.length === 0) {
        statusMessage.innerText = "Please select an image file";
        return;
    }

    // Ensure user data is available
    if (!userData.firstName || !userData.email) {
        statusMessage.innerText = "User data not found. Please log in again.";
        return;
    }

    // Show loading message
    statusMessage.innerHTML = '<span class="loading"></span> Uploading image...';
    
    // Get the file
    const file = fileInput.files[0];
    
    try {
        // Convert file to base64 for ImgBB API
        const reader = new FileReader();
        reader.readAsDataURL(file);
        
        reader.onload = async function() {
            try {
                // Get base64 data (remove the data:image/jpeg;base64, part)
                let base64Image = reader.result.split(',')[1];
                
                // Create form data with the correct parameters
                const formData = new FormData();
                formData.append("key", IMGBB_API_KEY);
                formData.append("image", base64Image);
                
                // Upload to ImgBB
                const response = await fetch("https://api.imgbb.com/1/upload", {
                    method: "POST",
                    body: formData
                });
                
                const data = await response.json();
                
                if (!data.success) {
                    throw new Error(data.error?.message || "Failed to upload image to ImgBB");
                }
                
                // Get image URL from ImgBB response
                const imageUrl = data.data.url;
                
                // Store in Firebase
                await addDoc(collection(db, "user_uploads"), {
                    username: userData.firstName,
                    email: userData.email,
                    socialUsername: socialUsername || "Not Provided",
                    image: imageUrl,
                    thumbnail: data.data.thumb?.url || imageUrl, // Store thumbnail if available
                    delete_url: data.data.delete_url || null,    // Store delete URL
                    timestamp: serverTimestamp()
                });
        
                statusMessage.innerText = "Image uploaded successfully!";
                fileInput.value = "";
                document.getElementById("socialUsername").value = "";
                document.getElementById("fileName").textContent = "No file selected";
                document.getElementById("imagePreview").style.display = "none";
            } catch (error) {
                console.error("Error uploading image: ", error);
                statusMessage.innerText = "Failed to upload image: " + error.message;
            }
        };
        
        reader.onerror = function(error) {
            console.error("Error reading file: ", error);
            statusMessage.innerText = "Failed to read image file. Please try again.";
        };
    } catch (error) {
        console.error("Error preparing image: ", error);
        statusMessage.innerText = "Failed to prepare image. Please try again.";
    }
});

// Logout function
document.getElementById("logout").addEventListener("click", () => {
    signOut(auth)
        .then(() => {
            window.location.href = "index.html"; // Redirect to login page
        })
        .catch((error) => {
            console.error("Error signing out: ", error);
        });
});