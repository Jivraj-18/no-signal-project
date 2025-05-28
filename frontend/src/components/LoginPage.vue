<template>
  <div class="login-page">
    <!-- Animated background -->
    <div class="background-overlay">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>

    <div class="login-container">
      <h1 class="title">Welcome Back</h1>
      <p class="subtitle">Continue your AI journey</p>

      <div class="login-box">
        <button @click="handleGoogleLogin" class="google-login-btn">
          <img src="/googleicon.png" alt="Google" class="google-icon" />
          <span>Continue with Google</span>
        </button>

        <div class="login-footer">
          <p>By continuing, you agree to our Terms of Service and Privacy Policy</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  methods: {
    handleGoogleLogin() {
      // Redirect to backend login route to initiate Google OAuth
      window.location.href = 'http://localhost:8000/login';
    }
  }
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #000310 0%, #531296 100%);
  position: relative;
  overflow: hidden;
}

/* Animated background */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  animation: floating 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 20%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 30%;
  left: 20%;
  animation-delay: 4s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 30%;
  animation-delay: 1s;
}

@keyframes floating {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.login-container {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 32px;
  max-width: 420px;
  width: 100%;
  animation: slideUp 0.8s ease-out;
}

.title {
  font-size: clamp(2rem, 6vw, 3rem);
  font-weight: 700;
  color: white;
  margin: 0 0 16px 0;
  line-height: 1.2;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 48px;
  font-weight: 400;
}

.login-box {
  background: linear-gradient(135deg, 
    rgba(0, 3, 16, 0.75) 0%, 
    rgba(83, 18, 150, 0.65) 100%
  );
  backdrop-filter: blur(16px);
  border-radius: 28px;
  padding: 32px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.google-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.google-login-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.google-icon {
  width: 24px;
  height: 24px;
  opacity: 0.9;
}

.login-footer {
  margin-top: 24px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  line-height: 1.5;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 480px) {
  .login-container {
    padding: 24px 16px;
  }
  
  .title {
    font-size: clamp(1.5rem, 8vw, 2.5rem);
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .login-box {
    padding: 24px;
  }
}
</style>
