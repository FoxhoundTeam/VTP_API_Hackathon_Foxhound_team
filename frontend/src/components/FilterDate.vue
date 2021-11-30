<template>
  <v-menu
    ref="menu"
    v-model="menu"
    :close-on-content-click="false"
    :return-value.sync="dates"
    transition="scale-transition"
    offset-y
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="strDates"
        label="Даты"
        prepend-icon="mdi-calendar"
        readonly
        v-bind="attrs"
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker v-model="dates" no-title scrollable range>
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="menu = false"> Отмена </v-btn>
      <v-btn
        text
        color="primary"
        @click="
          $refs.menu.save(dates);
          $emit('input', dates);
        "
      >
        OK
      </v-btn>
    </v-date-picker>
  </v-menu>
</template>

<script>
export default {
  props: ["value"],
  data() {
    return {
      dates: this.value,
      menu: false,
    };
  },
  computed: {
    strDates() {
      return this.dates[0] + " ~ " + this.dates[1];
    },
  },
  watch: {
    value() {
      this.dates = this.value;
    },
  },
};
</script>

<style>
</style>