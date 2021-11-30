<script>
import { Line, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  data() {
    return {
      options: {
        maintainAspectRatio: false,
        legend: {
          display: false,
        },
        elements: {
          line: {
            fill: false,
          },
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                stepSize: 1,
                suggestedMax: 3,
              },
            },
          ],
          xAxes: [
            {
              type: "time",
              time: {
                unit: "hour",
              },
            },
          ],
        },
      },
    };
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
  computed: {
    dates() {
      return this.$store.state.dates;
    },
  },
  watch: {
    async dates() {
      if (this.dates[0] == this.dates[1])
        await this.$set(this.options, "scales", {
          ...this.options.scales,
          xAxes: [
            {
              type: "time",
              time: {
                unit: "hour",
              },
            },
          ],
        });
      else
        await this.$set(this.options, "scales", {
          ...this.options.scales,
          xAxes: [
            {
              type: "time",
              time: {
                unit: "day",
              },
            },
          ],
        });
      this.$data._chart.options = this.options;
      await this.$data._chart.update();
    },
  },
};
</script>

<style>
</style>