<template>
  <div>
    <b-navbar toggleable="md">
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="/">
          Chainlink
      </b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav class="ml-auto">
          <b-nav-item href="/">Home</b-nav-item>
          <b-nav-item :href="'https://github.com/login/oauth/authorize?client_id=' + clientId">Sign in with Github</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<style>
#header-img {
  height: 70px;
  margin-right: 10px;
}
</style>

<script>
  export default {
    name: "Navbar",
    data () {
      return {
        // Github Client ID for this application
        clientId: ''
      }
    }
  }
</script>
