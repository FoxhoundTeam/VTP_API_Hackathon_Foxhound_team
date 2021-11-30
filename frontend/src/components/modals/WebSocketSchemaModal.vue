<template>
  <v-dialog
    v-model="show"
    fullscreen
    width="1000px"
    hide-overlay
    transition="dialog-bottom-transition"
    @click:outside="closeModal()"
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="closeModal()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title
          ><span class="text-h5">{{
            `${
              this.$route.params.id ? "Редактировать" : "Создать"
            } схему WebSocket`
          }}</span></v-toolbar-title
        >
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn text @click="save()">
            {{ $route.params.id ? "Сохранить" : "Создать" }}
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card-text>
        <v-text-field
          v-model="schema.name"
          label="Название"
          counter
          maxlength="512"
        ></v-text-field>
        <v-text-field
          v-model="schema.code"
          label="Код (необязательно)"
          counter
          maxlength="512"
        ></v-text-field>
        <v-text-field v-model="schema.method" label="Метод"></v-text-field>
        <h3>Схема данных</h3>
        <json-schema-editor lang="en_US" :value="schema.schema" />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data() {
    return {
      show: true,
      schema: {
        name: "",
        schema: {
          type: "object",
        },
      },
    };
  },
  beforeMount() {
    this.schema = {
      ...(this.$store.state.schemas[
        this.$store.state.schemas.findIndex(
          (v) => v.id == this.$route.params.id
        )
      ] || this.schema),
    };
    this.schema.schema = {
      root: this.schema.schema,
    };
  },
  methods: {
    closeModal() {
      this.show = false;
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "WebSocketSchema",
        query: q,
      });
    },
    async save() {
      this.schema.schema = this.schema.schema.root;
      if (this.schema.id) {
        await this.$store.dispatch("updateItem", {
          data: this.schema,
          dataID: this.schema.id,
          mutation: "setWebSocketSchemas",
          url: "WebSocketSchema",
          items_name: "schemas",
        });
      } else {
        await this.$store.dispatch("addItem", {
          data: this.schema,
          mutation: "setWebSocketSchemas",
          url: "WebSocketSchema",
          items_name: "schemas",
        });
      }
      this.closeModal();
    },
  },
};
</script>
<style>
</style>