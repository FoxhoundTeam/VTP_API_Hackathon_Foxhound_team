<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :items-per-page="3"
    class="elevation-1"
    dense
    :footer-props="{'disable-items-per-page': true}"
  >
    <template v-slot:top>
      <v-row>
        <v-col cols="6">
          <v-toolbar-title class="ml-5 mt-3">{{tableName}}</v-toolbar-title>
        </v-col>
        <v-col cols="6">
          <v-spacer></v-spacer>
          <v-btn
            class="mx-1 float-right"
            icon
            @click="$router.push({ name: urlName, query: {... $route.query, ...urlQuery} })"
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
  props: {
    headers: {
      type: Array,
    },
    items: {
      type: Array,
    },
    tableName: {
      type: String,
    },
    urlName: {
      type: String,
    },
    urlQuery: {
      type: Object,
      default: Object,
    }
  },
};
</script>

<style>
</style>