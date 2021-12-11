<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="filtereditems"
      :items-per-page="10"
      class="elevation-1"
      :footer-props="{ 'items-per-page-options': [5, 10, 15] }"
      @click:row="
        (row) =>
          $router.push({
            name: 'ViolationView',
            query: {
              ...$route.query,
            },
            params: {
              id: row.id,
            },
          })
      "
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="4">
            <v-toolbar-title class="ml-5 mt-3"
              >WebSocket нарушения</v-toolbar-title
            >
          </v-col>
          <v-col cols="8">
            <div class="d-flex align-items-center justify-content-end">
              <v-text-field
                prepend-icon="search"
                label="Поиск"
                v-model="search"
              ></v-text-field>
              <filter-date v-model="dates"></filter-date>
            </div>
          </v-col>
        </v-row>
      </template>
      <template v-slot:item.type="{item}">
        <span>{{types[item.type]}}</span>
      </template>
    </v-data-table>
    <router-view />
  </div>
</template>

<script>
import FilterDate from "../components/FilterDate.vue";
export default {
  components: { FilterDate },
  data() {
    return {
      search: "",
      types: {
        BO: "Bad origin",
        BM: "Bad method",
        SI: "SQL injection",
        X: "XSS attack",
        BW: "Bad word",
        IF: "Invalid message format",
        U: "Unknown exception",
        FL: "Personal data detected",
      },
      headers: [
        {
          text: "Время",
          value: "dttm",
        },
        {
          text: "Тип",
          value: "type",
        },
        { text: "Клиент", value: "client" },
        { text: "IP адрес", value: "source" },
      ],
    };
  },
  computed: {
    dates: {
      get() {
        return this.$store.state.dates;
      },
      set(value) {
        this.$store.commit("setDates", value);
      },
    },
    filtereditems() {
      return this.$store.state.violations.filter((item) => {
        return (
          item.source.toLowerCase().match(this.search.toLowerCase()) ||
          item.client.toLowerCase().match(this.search.toLowerCase())
        );
      });
    },
  },
  watch: {
    async dates() {
      await this.$store.dispatch("setViolations");
      if (
        this.$route.query.dt_from == this.dates[0] &&
        this.$route.query.dt_to == this.dates[1]
      )
        return;
      this.$router.replace({
        name: this.$route.name,
        query: {
          ...this.$route.query,
          dt_from: this.dates[0],
          dt_to: this.dates[1],
        },
      });
    },
  },
  async mounted() {
    if (!this.$store.state.violations.length) {
      this.dates = [
        this.$route.query.dt_from || new Date().toISOString().substr(0, 10),
        this.$route.query.dt_to || new Date().toISOString().substr(0, 10),
      ];
    }
  },
};
</script>

<style>
</style>