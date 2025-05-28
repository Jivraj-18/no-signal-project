<template>
  <div class="user-profile">
    <h1>User Profile</h1>
    <p>Welcome, {{ userName }}!</p>
    <p>Email: {{ userEmail }}</p>
  </div>
</template>

<script>
export default {
  name: 'UserProfilePage',
  data() {
    return {
      userName: 'John Doe',
      userEmail: 'johndoe@example.com'
    };
  }
};
</script>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  text-align: center;
}
</style>
