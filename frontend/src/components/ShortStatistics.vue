<template>
  <v-sheet :color="color" rounded="lg">
    <v-row>
      <v-col>
        <h6 class="text-light ml-3">{{ type }} {{ data }}</h6>
      </v-col>
      <v-col cols="2" v-if='icon'>
        <v-icon small color="white">{{ icon }}</v-icon>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script>
export default {
  props: ["color", "type", "data", "icon"],
};
</script>

<style>
</style>