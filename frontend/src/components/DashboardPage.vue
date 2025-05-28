<template>
  <div class="dashboard" @click="closeNavbar">
    <!-- Animated background -->
    <div class="background-overlay">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>

    <!-- Navigation toggle -->
    <div class="navbar-toggle" @click.stop="toggleNavbar">
      <div class="hamburger" :class="{ active: isNavbarOpen }">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>

    <!-- Side navigation -->
    <div class="navbar-overlay" :class="{ open: isNavbarOpen }" @click="closeNavbar"></div>
    <nav class="navbar" :class="{ open: isNavbarOpen }">
      <div class="navbar-header">
        <h3>Menu</h3>
      </div>
      <div class="navbar-content">
        <!-- Chat list -->
        <div class="chat-list">
          <button class="chat-row new-chat" @click="startNewChat">
            <span>New Chat</span>
            <img src="/iconpng.png" alt="New" class="plus-icon" />
          </button>
          <button class="chat-row" @click="loadChat('gdp')">
            <span class="chat-title">Indian's GDP now?</span>
          </button>
          <button class="chat-row" @click="loadChat('minister')">
            <span class="chat-title">Finance minister of India?</span>
          </button>
        </div>
        
        <!-- Footer buttons -->
        <div class="navbar-footer">
          <button class="navbar-item" @click="handleNavClick('profile')">
            <div class="nav-icon">👤</div>
            <span>Profile</span>
          </button>
          <button class="navbar-item" @click="handleNavClick('pro')">
            <div class="nav-icon">⭐</div>
            <span>Buy Pro</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main content area -->
    <div class="main-layout">
      <!-- Content section -->
      <div class="content-area" :class="{ 'has-output': queryResponse }">
        <div class="greeting-container" v-if="!queryResponse">
          <h1 class="greeting-text" :key="animatedText">{{ animatedText }}</h1>
          <div class="subtitle">Powered by AI • Fast • Accurate</div>
        </div>
        
        <div class="output-container" v-if="queryResponse">
          <div class="output-header">
            <button class="clear-chat-btn" @click="clearChat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
              </svg>
              Clear Chat
            </button>
          </div>
          <div class="output-content">
            {{ queryResponse }}
          </div>
        </div>
      </div>

      <!-- Fixed query input section -->
      <div class="query-section-fixed">
        <div class="query-container">
          <div class="input-wrapper">
            <textarea
              v-model="textQuery"
              placeholder="Ask me anything..."
              class="query-input"
              @keydown.enter.prevent="submitQuery"
              @focus="isInputFocused = true"
              @blur="isInputFocused = false"
              rows="1"
            ></textarea>
            <button 
              class="send-button" 
              @click="submitQuery"
              :disabled="!textQuery.trim()"
              :class="{ active: textQuery.trim() }"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="m22 2-7 20-4-9-9-4 20-7z"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Quick suggestions - only show when no output -->
        <div class="quick-suggestions" v-if="!queryResponse">
          <button 
            v-for="suggestion in suggestions" 
            :key="suggestion"
            class="suggestion-chip"
            @click="selectSuggestion(suggestion)"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  data() {
    return {
      textQuery: '',
      isNavbarOpen: false,
      isInputFocused: false,
      animatedText: 'Welcome to the Future of AI',
      textOptions: [
        'Welcome to the Future of AI',
        'Ask Anything, Get Everything',
        'Intelligent Answers in Seconds',
        'Your AI Assistant Awaits'
      ],
      textIndex: 0,
      suggestions: [
        'How does AI work?',
        'Write a creative story',
        'Explain quantum physics',
        'Plan my day'
      ],
      queryResponse: null
    };
  },
  methods: {
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    closeNavbar() {
      this.isNavbarOpen = false;
    },
    handleClickOutside(event) {
      const navbar = this.$el.querySelector('.navbar');
      const toggleButton = this.$el.querySelector('.navbar-toggle');
      if (this.isNavbarOpen && !navbar.contains(event.target) && !toggleButton.contains(event.target)) {
        this.closeNavbar();
      }
    },
    submitQuery() {
  if (!this.textQuery.trim()) return;

  const formData = new FormData();
  formData.append("question", this.textQuery);

  fetch("http://127.0.0.1:8000/process", {
    method: "POST",
    body: formData,
    credentials: "include", 
  })
  .then(response => {
    if (!response.ok) throw new Error("Network response was not ok");
    return response.json();  // wait for JSON to be parsed
  })
  .then(data => {
    console.log("Response received:", data);
    this.queryResponse = data;  // now assign the parsed response
    this.textQuery = '';
  })
  .catch(error => {
    console.error("Error submitting query:", error);
  });
}


,
    selectSuggestion(suggestion) {
      this.textQuery = suggestion;
      this.submitQuery();
    },
    clearChat() {
      this.queryResponse = null;
    },
    handleNavClick(action) {
      console.log(`${action} clicked`);
      this.closeNavbar();
      // Add navigation logic here
    },
    cycleText() {
      this.textIndex = (this.textIndex + 1) % this.textOptions.length;
      this.animatedText = this.textOptions[this.textIndex];
    },
    autoResizeTextarea() {
      const textarea = this.$el.querySelector('.query-input');
      if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
      }
    }
  },
  watch: {
    textQuery() {
      this.$nextTick(() => {
        this.autoResizeTextarea();
      });
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
    this.textCycleInterval = setInterval(this.cycleText, 4000);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
    clearInterval(this.textCycleInterval);
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
  box-sizing: border-box;
}

.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
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

/* Navigation */
.navbar-toggle {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 1001;
  cursor: pointer;
  padding: 8px;
}

.hamburger {
  display: flex;
  flex-direction: column;
  width: 24px;
  height: 18px;
  justify-content: space-between;
  cursor: pointer;
}

.hamburger span {
  display: block;
  height: 2px;
  width: 100%;
  background: white;
  border-radius: 1px;
  transition: all 0.3s ease;
}

.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

.navbar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 999;
}

.navbar-overlay.open {
  opacity: 1;
  visibility: visible;
}

.navbar {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 320px;
  background: linear-gradient(135deg, rgba(0, 3, 16, 0.95) 0%, rgba(83, 18, 150, 0.95) 100%);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(83, 18, 150, 0.3);
  transform: translateX(100%);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.navbar.open {
  transform: translateX(0);
}

.navbar-header {
  padding: 32px 24px 24px;
  border-bottom: 1px solid rgba(83, 18, 150, 0.3);
}

.navbar-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: white;
}

.navbar-content {
  display: flex;
  flex-direction: column;
  padding: 16px;
  height: calc(100vh - 80px);
}

.chat-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
}

.chat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;
  height: 36px;
  font-size: 14px;
}

.chat-row:hover {
  background: rgba(255, 255, 255, 0.1);
}

.new-chat {
  background: rgba(83, 18, 150, 0.3);
}

.new-chat span {
  margin-right: auto;
}

.plus-icon {
  width: 20px;
  height: 20px;
  opacity: 0.9;
  margin-left: 8px;
}

.chat-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.navbar-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.navbar-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: transparent;
  border: none;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.9);
  text-align: left;
}

.navbar-item:hover {
  background: rgba(83, 18, 150, 0.3);
  transform: translateX(4px);
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

/* Main layout */
.main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  z-index: 1;
}

/* Content area */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 80px 24px 20px; /* Top padding for navbar toggle */
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.content-area.has-output {
  padding-bottom: 140px; /* Space for fixed input */
}

.greeting-container {
  text-align: center;
  max-width: 800px;
  margin-top: 10vh;
}

.greeting-text {
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 700;
  color: white;
  margin: 0 0 16px 0;
  line-height: 1.2;
  animation: slideUp 0.8s ease-out;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
  animation: slideUp 0.8s ease-out 0.2s both;
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

/* Output container */
.output-container {
  width: 100%;
  max-width: 900px;
  background: linear-gradient(135deg, #000310 0%, #531296 100%);
  /* background: linear-gradient(135deg, 
    rgba(0, 3, 16, 0.85) 0%, 
    rgba(83, 18, 150, 0.75) 100%
  ); */
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  animation: slideUp 0.6s ease-out;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.output-header {
  padding: 20px 24px 0;
  display: flex;
  justify-content: flex-end;
}

.clear-chat-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-chat-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-1px);
}

.output-content {
  color: rgba(255, 255, 255, 0.95);
  font-size: 16px;
  line-height: 1.7;
  letter-spacing: 0.2px;
  font-weight: 400;
  white-space: pre-wrap;
  padding: 20px 32px 32px;
  max-height: 60vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.output-content::-webkit-scrollbar {
  width: 6px;
}

.output-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.output-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  transition: background-color 0.3s ease;
}

.output-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* Fixed query section */
.query-section-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 20px 24px 32px;
  background-color: transparent;
  backdrop-filter: blur(10px);
}

.query-container {
  max-width: 800px;
  margin: 0 auto;
  background: #4e267d;
  border-radius: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(255, 255, 255, 0.15);
  position: relative;
  overflow: hidden;
}

.query-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
}

.query-container:focus-within {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.3);
  background: #542d8a;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px;
}

.query-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  font-weight: 400;
  padding: 16px 20px;
  background: transparent;
  resize: none;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.95);
  min-height: 60px;
  max-height: 120px;
  font-family: inherit;
  letter-spacing: 0.3px;
}

.query-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
  font-weight: 300;
}

.send-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 14px;
  margin-right: 4px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0.7;
  width: 50px;
  height: 50px;
}

.send-button:disabled {
  cursor: not-allowed;
  opacity: 0.3;
}

.send-button.active {
  opacity: 1;
  background: rgba(255, 255, 255, 0.15);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
}

/* Quick suggestions */
.quick-suggestions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.suggestion-chip {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 14px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 400;
}

.suggestion-chip:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Responsive design */
@media (max-width: 768px) {
  .navbar {
    width: 100vw;
    max-width: 320px;
  }
  
  .query-section-fixed {
    padding: 16px 16px 24px;
  }
  
  .content-area {
    padding: 80px 16px 20px;
  }
  
  .content-area.has-output {
    padding-bottom: 160px;
  }
  
  .greeting-text {
    font-size: clamp(1.5rem, 8vw, 2.5rem);
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .output-container {
    margin: 0;
  }
  
  .output-content {
    padding: 16px 20px 24px;
  }
  
  .quick-suggestions {
    gap: 8px;
  }
  
  .suggestion-chip {
    font-size: 13px;
    padding: 6px 12px;
  }
}

@media (max-width: 480px) {
  .navbar-toggle {
    top: 16px;
    right: 16px;
  }
  
  .query-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
  
  .content-area.has-output {
    padding-bottom: 180px;
  }
}
</style>