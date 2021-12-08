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
            name: 'FileInfoView',
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
              >Файловые проверки</v-toolbar-title
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
              <v-checkbox
                label="Только нарушения"
                dense
                v-model="onlyViolations"
                class="mr-2"
              />
            </div>
          </v-col>
        </v-row>
      </template>
      <template v-slot:item.status="{ item }">
        <v-icon :color="status_icon_and_color[item.status][1]">{{
          status_icon_and_color[item.status][0]
        }}</v-icon>
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
      status_icon_and_color: {
        P: ["mdi-progress-clock", "orange"],
        O: ["done", "green"],
        E: ["error", "orange"],
        V: ["warning", "red"],
      },
      headers: [
        {
          text: "Время загрузки",
          value: "dttm_loaded",
        },
        {
          text: "Тип файла",
          value: "file_type",
        },
        { text: "IP адрес", value: "source" },
        { text: "Статус", value: "status" },
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
    onlyViolations: {
      get() {
        return String(this.$route.query.onlyViolations) == 'true';
      },
      set(value) {
        this.$router.replace({
          name: this.$route.name,
          query: {
            ...this.$route.query,
            onlyViolations: String(value),
          },
        });
      },
    },
    filtereditems() {
      let _this = this;
      return this.$store.state.fileInfos.filter((item) => {
        return (
          item.source.toLowerCase().match(this.search.toLowerCase()) ||
          item.client.toLowerCase().match(this.search.toLowerCase()) ||
          item.name.toLowerCase().match(this.search.toLowerCase())
        ) && (_this.onlyViolations ? item.status == 'V': true);
      });
    },
  },
  watch: {
    async dates() {
      await this.$store.dispatch("setFileInfo");
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
    if (!this.$store.state.fileInfos.length) {
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