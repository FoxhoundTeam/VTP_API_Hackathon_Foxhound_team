<template>
  <v-container>
    <v-row>
      <v-col cols="3">
        <filter-data-card v-model="dates"></filter-data-card>
        <short-statistics
          class="mb-4"
          :data="$store.state.webSocketSchemaCount"
          type="Количество WebSocket схем:"
          color="primary"
        ></short-statistics>
        <short-statistics
          class="my-4"
          :data="$store.state.httpAllowedTypeCount"
          type="Количество HTTP:"
          color="#dbb838"
        ></short-statistics>
        <short-statistics
          class="my-4"
          :data="$store.state.violationsCount"
          type="Количество нарушений:"
          icon="report_problem"
          color="#d9544f"
        ></short-statistics>
      </v-col>
      <v-col cols="9">
        <v-card>
          <v-card-title> Количество нарушений </v-card-title>
          <small-chart :chartData="$store.state.chart"></small-chart>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <small-violators-table></small-violators-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FilterDataCard from "../components/FilterDataCard.vue";
import ShortStatistics from "../components/ShortStatistics.vue";
import SmallChart from "../components/Chart.vue";
import SmallViolatorsTable from "../components/SmallViolatorsTable.vue";
export default {
  components: {
    FilterDataCard,
    ShortStatistics,
    SmallChart,
    SmallViolatorsTable,
  },
  data() {
    return {};
  },
  computed: {
    dates: {
      get() {
        return this.$store.state.dates;
      },
      set(value) {
        this.$store.commit("setDates", value);
        this.$router.replace({
          name: this.$route.name,
          query: { type: this.$store.state.periodType, dt_from: this.dates[0], dt_to: this.dates[1] },
        });
      },
    },
  },
  watch: {
    async dates() {
      await this.$store.dispatch("setViolations");
      await this.$store.dispatch("setChart");
    },
  },
  async mounted() {
    if (!this.$store.state.camerasCount) {
      let dates = [
        this.$route.query.dt_from || new Date().toISOString().substr(0, 10),
        this.$route.query.dt_to || new Date().toISOString().substr(0, 10),
      ];
      if (this.$route.query.type) {
        this.$store.commit("setPeriodType", Number(this.$route.query.type));
      }
      if (this.$route.query.type == "4" || !this.$route.query.type || !this.dates.length) {
        this.dates = dates;
      }

      await this.$store.dispatch("setWebSocketSchemaStat");
      await this.$store.dispatch("setHTTPAllowedTypeStat");
    }
  },
};
</script>

<style>
</style>