<template>
  <v-dialog v-model="show" max-width="800px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">{{
            `${
              this.$route.params.id ? "Редактировать" : "Создать"
            } файловый прокси`
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="proxy.proxy_url"
            label="URL"
            counter
            maxlength="1024"
          ></v-text-field>
          <h3>Заголовки</h3>
          <v-container>
            <v-row v-for="(tag, i) in proxy.headers" :key="i">
              <v-col class="my-0 py-0" cols="6">
                <v-text-field
                  v-model="proxy.headers[i].name"
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
                  v-model="proxy.headers[i].value"
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
      proxy: {
        proxy_url: "",
        headers: {},
      },
    };
  },
  beforeMount() {
    this.proxy = {
      ...(this.$store.state.filesProxies[
        this.$store.state.filesProxies.findIndex(
          (v) => v.id == this.$route.params.id
        )
      ] || this.proxy),
    };
    var headers = [];
    for (let header_name in this.proxy.headers) {
      headers.push({
        name: header_name,
        value: this.proxy.headers[header_name],
      });
    }
    this.$set(this.proxy, "headers", headers);
  },
  methods: {
    closeModal() {
      this.show = false;
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "FileProxy",
        query: q,
      });
    },
    async save() {
      var headers = {};
      for (let header of this.proxy.headers) {
        headers[header.name] = header.value;
      }
      this.proxy.headers = headers;
      if (this.proxy.id) {
        await this.$store.dispatch("updateItem", {
          data: this.proxy,
          dataID: this.proxy.id,
          mutation: "setFileProxies",
          url: "FileProxy",
          items_name: "filesProxies",
        });
      } else {
        await this.$store.dispatch("addItem", {
          data: this.proxy,
          mutation: "setFileProxies",
          url: "FileProxy",
          items_name: "filesProxies",
        });
      }
      this.closeModal();
    },
    addItem() {
      this.proxy.headers.push({ name: "", value: "" });
    },
    deleteItem(i) {
      this.proxy.headers.splice(i, 1);
    },
  },
};
</script>
<style>
</style>