<template>
  <v-dialog v-model="show" width="800px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">{{
            `Информация о проверке файла ${file_info.name}`
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="file_info.dttm_loaded"
            label="Время загрузки"
            readonly
            prepend-icon="mdi-calendar"
          ></v-text-field>
          <v-text-field
            :value="status_text[file_info.status]"
            label="Статус"
            readonly
          ></v-text-field>
          <v-text-field
            v-if="file_info.dttm_end_check"
            v-model="file_info.dttm_end_check"
            label="Время окончания проверки"
            readonly
            prepend-icon="mdi-calendar"
          ></v-text-field>
          <v-text-field
            v-model="file_info.file_type"
            label="Тип файла"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="file_info.source"
            label="IP адрес"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="file_info.client"
            label="Клиент"
            readonly
          ></v-text-field>
          <v-textarea
            v-model="file_info.message"
            label="Сообщение проверки"
            readonly
          ></v-textarea>
          <p>
            Сылка для скачивания:
            <a :href="file_info.file_url">{{ file_info.file_url }}</a>
          </p>
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
      status_text: {
        P: "В процессе",
        O: "Ок",
        E: "Ошибка",
        V: "Нарушение",
      },
    };
  },
  computed: {
    file_info() {
      return {
        ...this.$store.state.fileInfos[
          this.$store.state.fileInfos.findIndex(
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
        name: "FileInfo",
        query: q,
      });
    },
  },
};
</script>
<style>
</style>