<template>
  <v-data-table
    :headers="headers"
    :items="$store.state.violations"
    :items-per-page="3"
    class="elevation-1"
    dense
    :footer-props="{'disable-items-per-page': true}"
  >
    <template v-slot:top>
      <v-row>
        <v-col cols="6">
          <v-toolbar-title class="ml-5 mt-3">Нарушения</v-toolbar-title>
        </v-col>
        <v-col cols="6">
          <v-spacer></v-spacer>
          <v-btn
            class="mx-1 float-right"
            icon
            @click="$router.push({ name: 'Violation', query: {... $route.query} })"
          >
            <v-icon color="gray"> open_in_full </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </v-data-table>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: "Время",
          value: "dttm",
        },
        { text: "Клиент", value: "client" },
        { text: "IP адрес", value: "source" },
      ],
    };
  },
};
</script>

<style>
</style>