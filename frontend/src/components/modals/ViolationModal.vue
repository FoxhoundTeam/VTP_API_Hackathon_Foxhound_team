<template>
  <v-dialog v-model="show" width="800px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">{{
            `Нарушение № ${this.$route.params.id}`
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="violation.dttm"
            label="Время"
            readonly
            prepend-icon="mdi-calendar"
          ></v-text-field>
          <v-text-field
            v-model="violation.source"
            label="IP адрес"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="violation.client"
            label="Клиент"
            readonly
          ></v-text-field>
          <v-textarea
            v-model="violation.message"
            label="Причина нарушения"
            readonly
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeModal()">
            Закрыть
          </v-btn>
        </v-card-actions>
      </template>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data() {
    return {
      show: true,
    };
  },
  computed: {
    violation() {
      return {
        ...this.$store.state.violations[
          this.$store.state.violations.findIndex(
            (v) => v.id == this.$route.params.id
          )
        ],
      };
    },
  },
  methods: {
    closeModal() {
      this.show = false;
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "Violation",
        query: q,
      });
    },
  },
};
</script>
<style>
</style>