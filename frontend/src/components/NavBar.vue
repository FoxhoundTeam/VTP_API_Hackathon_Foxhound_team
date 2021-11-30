<template>
  <div>
    <v-navigation-drawer
      permanent
      expand-on-hover
      clipped
      mini-variant
      app
      v-if="$store.state.isAuthenticated"
    >
      <v-list nav dense active-class="deep-purple--text text--accent-4">
        <v-list-item link :to="{name: 'Dashboard', query: {...$route.query}}">
          <v-list-item-icon>
            <v-icon>leaderboard</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Дашборд</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link :to="{name: 'Violation', query: {...$route.query}}">
          <v-list-item-icon>
            <v-icon>report_problem</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Нарушения</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link to="/websocket">
          <v-list-item-icon>
            <v-icon>schema</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Схемы WebSocket</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link to="/websocket_callback">
          <v-list-item-icon>
            <v-icon>schema</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>WebSocket Callbacks</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link to="/http">
          <v-list-item-icon>
            <v-icon>http</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>HTTP</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link to="/settings">
          <v-list-item-icon>
            <v-icon>settings</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Настройки</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-group prepend-icon="person">
          <template v-slot:activator>
            <v-list-item-title>Пользователь</v-list-item-title>
          </template>

          <v-list-item @click="$store.dispatch('logout')"
            ><v-list-item-icon>
              <v-icon>logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Выйти</v-list-item-title>
            </v-list-item-content></v-list-item
          >
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left>
      <v-app-bar-title>FoxWall</v-app-bar-title>
    </v-app-bar>
  </div>
</template>

<script>
export default {};
</script>

<style>
</style>