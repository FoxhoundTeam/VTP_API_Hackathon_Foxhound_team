<template>
  <v-dialog v-model="show" max-width="800px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">{{
            `${
              this.$route.params.id ? "Редактировать" : "Создать"
            } WebSocketCallback`
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="callback.callback_url"
            label="URL"
            counter
            maxlength="1024"
          ></v-text-field>
          <v-text-field
            v-model="callback.method"
            label="Метод"
            counter
            maxlength="512"
          ></v-text-field>
          <h3>Заголовки</h3>
          <v-container>
            <v-row v-for="(tag, i) in callback.headers" :key="i">
              <v-col class="my-0 py-0" cols="6">
                <v-text-field
                  v-model="callback.headers[i].name"
                  rounded
                  filled
                ></v-text-field>
              </v-col>
              <v-col class="my-0 py-0" cols="6">
                <v-text-field
                  rounded
                  filled
                  append-icon="delete"
                  @click:append="deleteItem(i)"
                  v-model="callback.headers[i].value"
                >
                </v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                ><v-btn class="mx-1" icon @click="addItem()">
                  <v-icon color="gray"> add </v-icon>
                </v-btn></v-col
              >
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeModal()">
            Закрыть
          </v-btn>
          <v-btn color="blue darken-1" text @click="save()">
            {{ $route.params.id ? "Сохранить" : "Создать" }}
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
      callback: {
        callback_url: "",
        headers: {},
        method: "",
      },
    };
  },
  beforeMount() {
    this.callback = {
      ...(this.$store.state.callbacks[
        this.$store.state.callbacks.findIndex(
          (v) => v.id == this.$route.params.id
        )
      ] || this.callback),
    };
    var headers = [];
    for (let header_name in this.callback.headers) {
      headers.push({
        name: header_name,
        value: this.callback.headers[header_name],
      });
    }
    this.$set(this.callback, "headers", headers);
  },
  methods: {
    closeModal() {
      this.show = false;
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "WebSocketCallback",
        query: q,
      });
    },
    async save() {
      var headers = {};
      for (let header of this.callback.headers) {
        headers[header.name] = header.value;
      }
      this.callback.headers = headers;
      if (this.callback.id) {
        await this.$store.dispatch("updateItem", {
          data: this.callback,
          dataID: this.callback.id,
          mutation: "setWebSocketCallbackss",
          url: "WebSocketCallback",
          items_name: "callbacks",
        });
      } else {
        await this.$store.dispatch("addItem", {
          data: this.callback,
          mutation: "setWebSocketCallbackss",
          url: "WebSocketCallback",
          items_name: "callbacks",
        });
      }
      this.closeModal();
    },
    addItem() {
      this.callback.headers.push({ name: "", value: "" });
    },
    deleteItem(i) {
      this.callback.headers.splice(i, 1);
    },
  },
};
</script>
<style>
</style>