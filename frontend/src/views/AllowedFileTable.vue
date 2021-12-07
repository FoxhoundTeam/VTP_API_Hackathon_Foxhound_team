<template>
  <div>
    <v-data-table
      :loading="loading"
      disable-sort
      class="elevation-1"
      :items="$store.state.allowedFiles"
      :headers="headers"
      @click:row="
        (row) =>
          $router.push({
            name: 'AllowedFileEdit',
            query: {
              ...$route.query,
            },
            params: {
              id: row.id,
            },
          })
      "
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="6">
            <v-toolbar-title class="ml-5 mt-3"
              >Разрешенные файлы</v-toolbar-title
            >
          </v-col>
          <v-col cols="6">
            <div class="d-flex align-items-center justify-content-end">
              <v-tooltip bottom open-delay="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mx-1"
                    v-bind="attrs"
                    v-on="on"
                    icon
                    @click="
                      $router.push({
                        name: 'AllowedFileCreate',
                        query: {
                          ...$route.query,
                        },
                      })
                    "
                  >
                    <v-icon color="gray" v-bind="attrs" v-on="on"> add </v-icon>
                  </v-btn>
                </template>
                <span>Добавить</span>
              </v-tooltip>
            </div>
          </v-col>
        </v-row>
      </template>
      <template v-slot:item.max_size="{ item }">
        <span>{{ `${item.max_size} ${sizes[item.size_mul]}` }}</span>
      </template>
    </v-data-table>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      sizes: {
        1: "байт",
        1024: "Кбайт",
        1048576: "Мбайт",
        1073741824: "Гбайт",
        1099511627776: "Тбайт",
      },
      headers: [
        {
          text: "Тип файла",
          value: "file_type",
        },
        {
          text: "Максимальная глубина",
          value: "max_depth",
        },
        {
          text: "Максимальный размер",
          value: "max_size",
        },
      ],
      loading: true,
      search: "",
    };
  },
  async beforeMount() {
    this.loading = true;
    if (this.$store.state.allowedFiles.length == 0) {
      await this.$store.dispatch("setAllowedFiles");
    }
    this.loading = false;
  },
};
</script>

<style>
</style>