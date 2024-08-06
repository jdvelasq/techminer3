from techminer3.plots.bar_chart import BarChart
from techminer3.plots.column_chart import ColumnChart
from techminer3.plots.line_chart import LineChart

from .command_interface import CommandInterface


class PlotCommand(CommandInterface):
    plot_types = {
        "columnchart": ColumnChart,
        "barchart": BarChart,
        "linechart": LineChart,
    }

    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser("plot", help="Plot data")
        parser.add_argument(
            "chart_type",
            help="Type of chart to create",
            choices=[
                "columnchart",
                "barchart",
                "linechart",
            ],
        )

    def execute(self):
        plot_class = self.plot_types.get(self.args.chart_type)
        if plot_class:
            plot_instance = plot_class()
            plot_instance.plot()
        else:
            print(f"Unknown chart type: {self.args.chart_type}")
