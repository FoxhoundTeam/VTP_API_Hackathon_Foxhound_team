<template>
  <div>
    <v-data-table
      :loading="loading"
      disable-sort
      class="elevation-1"
      :items="$store.state.schemas"
      :headers="headers"
      @click:row="
        (row) =>
          $router.push({
            name: 'WebSocketSchemaEdit',
            query: {
              ...$route.query,
            },
            params: {
              id: row.id,
            },
          })
      "
      :search="search"
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="6">
            <v-toolbar-title class="ml-5 mt-3"
              >Схемы WebSocket</v-toolbar-title
            >
          </v-col>
          <v-col cols="6">
            <div class="d-flex align-items-center justify-content-end">
              <v-text-field
                prepend-icon="search"
                label="Поиск"
                v-model="search"
              ></v-text-field>
              <v-tooltip bottom open-delay="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mx-1"
                    v-bind="attrs"
                    v-on="on"
                    icon
                    @click="
                      $router.push({
                        name: 'WebSocketSchemaCreate',
                        query: {
                          ...$route.query,
                        },
                      })
                    "
                  >
                    <v-icon color="gray" v-bind="attrs" v-on="on"> add </v-icon>
                  </v-btn>
                </template>
                <span>Добавить</span>
              </v-tooltip>
            </div>
          </v-col>
        </v-row>
      </template>
    </v-data-table>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "Название",
          value: "name",
        },
        {
          text: "Метод",
          value: "method",
        },
      ],
      loading: true,
      search: "",
    };
  },
  async beforeMount() {
    this.loading = true;
    if (this.$store.state.schemas.length == 0) {
      await this.$store.dispatch("setWebSocketSchemas");
    }
    this.loading = false;
  },
};
</script>

<style>
</style>