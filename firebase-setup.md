# Firebase Setup Instructions

## 1. Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click "Create a project"
3. Name: "healthy-india-app"
4. Enable Google Analytics (optional)

## 2. Enable Authentication
1. In Firebase Console → Authentication
2. Click "Get started"
3. Go to "Sign-in method" tab
4. Enable:
   - Email/Password
   - Google
   - Facebook
   - Twitter

## 3. Get Configuration
1. Project Settings → General
2. Scroll to "Your apps"
3. Click "Web" icon
4. Register app: "Healthy India Web"
5. Copy the config object

## 4. Update auth.html
Replace the firebaseConfig object with your actual config:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "your-sender-id",
    appId: "your-app-id"
};
```

## 5. Configure OAuth Providers

### Google
- Already configured with Firebase

### Facebook
1. Go to https://developers.facebook.com/
2. Create app → Consumer
3. Add Facebook Login product
4. In Firebase Console → Authentication → Sign-in method → Facebook
5. Add App ID and App Secret from Facebook

### Twitter/X
1. Go to https://developer.twitter.com/
2. Create project and app
3. Get API Key and API Secret
4. In Firebase Console → Authentication → Sign-in method → Twitter
5. Add API Key and API Secret

## 6. Set Authorized Domains
In Firebase Console → Authentication → Settings → Authorized domains
Add your domain (e.g., localhost for testing)

## 7. Test
1. Start your backend
2. Open auth.html
3. Try all login methods