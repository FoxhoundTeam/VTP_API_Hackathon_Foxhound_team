<template>
  <v-sheet>
    <v-select
      :items="choices"
      v-model="choice"
      label="Период"
      outlined
      item-text="type"
      item-value="value"
    ></v-select>
    <filter-date v-if="choice == 4" v-model="dates"></filter-date>
  </v-sheet>
</template>

<script>
import FilterDate from "./FilterDate.vue";
export default {
  components: { FilterDate },
  props: ["value"],
  data() {
    return {
      dates: this.value,
      menu: false,
      choices: [
        {
          type: "Сегодня",
          value: 1,
        },
        {
          type: "Вчера",
          value: 2,
        },
        {
          type: "Месяц",
          value: 3,
        },
        {
          type: "Произвольный интервал",
          value: 4,
        },
      ],
    };
  },
  computed: {
    strDates() {
      return this.dates[0] + " ~ " + this.dates[1];
    },
    choice: {
      get() {
        return this.$store.state.periodType;
      },
      set(value) {
        this.$store.commit("setPeriodType", value);

        this.$router.replace({
          name: this.$route.name,
          query: { type: value, dt_from: this.dates[0], dt_to: this.dates[1] },
        });
      },
    },
  },
  watch: {
    dates() {
      this.$emit("input", this.dates);
    },
    value() {
        if (this.value != this.dates)
            this.dates = this.value;
    },
    choice() {
      var date, dt_from, dt_to;
      switch (this.choice) {
        case 1:
          date = new Date().toISOString().substr(0, 10);
          this.dates = [date, date];
          break;
        case 2:
          date = new Date();
          date.setDate(date.getDate() - 1);
          date = date.toISOString().substr(0, 10);
          this.dates = [date, date];
          break;
        case 3:
          dt_from = new Date();
          dt_from.setDate(1);
          dt_to = new Date(dt_from.getFullYear(), dt_from.getMonth() + 1, 0);
          this.dates = [
            dt_from.toISOString().substr(0, 10),
            dt_to.toISOString().substr(0, 10),
          ];
          break;
        case 4:
            // dt_from = new Date();
            // dt_from.setDate(1);
            // dt_to = new Date(dt_from.getFullYear(), dt_from.getMonth() + 1, 0);
            // this.dates = [
            //   dt_from.toISOString().substr(0, 10),
            //   dt_to.toISOString().substr(0, 10),
            // ];
          break;
        default:
          break;
      }
    },
  },
};
</script>

<style>
</style>