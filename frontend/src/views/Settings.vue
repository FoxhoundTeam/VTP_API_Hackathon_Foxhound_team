<template>
  <v-card>
    <v-card-title>Настройки</v-card-title>
    <v-card-text>
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <v-combobox
              v-model="allowedOrigins"
              label="Разрешенные WebSocket Origins"
              multiple
              outlined
            >
              <template v-slot:selection="{ attrs, item, parent }">
                <v-chip
                  v-bind="attrs"
                  label
                  close
                  @click:close="parent.selectItem(item)"
                >
                  <span class="pr-2">
                    {{ item }}
                  </span>
                </v-chip>
              </template>
            </v-combobox>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-combobox
              v-model="filesProxies"
              label="Прокси для файлов"
              multiple
              outlined
            >
              <template v-slot:selection="{ attrs, item, parent }">
                <v-chip
                  v-bind="attrs"
                  label
                  close
                  @click:close="parent.selectItem(item)"
                >
                  <span class="pr-2">
                    {{ item }}
                  </span>
                </v-chip>
              </template>
            </v-combobox>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  computed: {
    allowedOrigins: {
      get() {
        return this.$store.state.wsAllowedOrigins.map((x) => x.name);
      },
      async set(value) {
        await this.$store.dispatch(
          "setNewWsAllowedOrigins",
          value.map((x) => {
            return { name: x };
          })
        );
      },
    },
    filesProxies: {
      get() {
        return this.$store.state.filesProxies.map((x) => x.proxy_url);
      },
      async set(value) {
        await this.$store.dispatch(
          "setNewFilesProxies",
          value.map((x) => {
            return { proxy_url: x };
          })
        );
      },
    },
  },
  async beforeMount() {
    if (this.$store.state.wsAllowedOrigins.length == 0) {
      await this.$store.dispatch("setWsAllowedOrigins");
    }
    if (this.$store.state.filesProxies.length == 0) {
      await this.$store.dispatch("setFilesProxies");
    }
  },
};
</script>

<style>
</style>