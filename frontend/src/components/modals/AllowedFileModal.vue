<template>
  <v-dialog v-model="show" max-width="800px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">{{
            `${
              this.$route.params.id ? "Редактировать" : "Создать"
            } разрешенный файл`
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="allowedFile.file_type"
            label="Тип файла"
            :items="fileTypes"
          />
          <v-text-field
            v-model="allowedFile.max_depth"
            label="Максимальная глубина"
          />
          <v-row>
            <v-col cols="8">
              <v-text-field
                v-model="allowedFile.max_size"
                label="Максимальный размер"
              />
            </v-col>
            <v-col cols="4"
              ><v-select
                v-model="allowedFile.size_mul"
                label="Единица измерения"
                :items="sizes"
                item-text="size"
                item-value="value"
            /></v-col>
          </v-row>
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
      fileTypes: ["xml", "json", "pdf", "exe", "zip"],
      sizes: [
        { value: 1, size: "байт" },
        { value: 1024, size: "Кбайт" },
        { value: 1048576, size: "Мбайт" },
        { value: 1073741824, size: "Гбайт" },
        { value: 1099511627776, size: "Тбайт" },
      ],
      allowedFile: {
        file_type: "PDF",
        size_mul: 1,
      },
    };
  },
  beforeMount() {
    this.allowedFile = {
      ...(this.$store.state.allowedFiles[
        this.$store.state.allowedFiles.findIndex(
          (v) => v.id == this.$route.params.id
        )
      ] || this.allowedFile),
    };
  },
  methods: {
    closeModal() {
      this.show = false;
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "AllowedFile",
        query: q,
      });
    },
    async save() {
      if (this.allowedFile.id) {
        await this.$store.dispatch("updateItem", {
          data: this.allowedFile,
          dataID: this.allowedFile.id,
          mutation: "setAllowedFiles",
          url: "AllowedFile",
          items_name: "allowedFiles",
        });
      } else {
        await this.$store.dispatch("addItem", {
          data: this.allowedFile,
          mutation: "setAllowedFiles",
          url: "AllowedFile",
          items_name: "allowedFiles",
        });
      }
      this.closeModal();
    },
  },
};
</script>
<style>
</style>