from ydata_profiling.report.presentation.core.correlation_table import CorrelationTable
from ydata_profiling.report.presentation.flavours.html import templates

#
# class HTMLCorrelationTable(CorrelationTable):
#     def render(self) -> str:
#         correlation_matrix_html = self.content["correlation_matrix"].to_html(
#             classes="correlation-table table table-striped",
#             float_format="{:.3f}".format
#         )
#         return templates.template("correlation_table.html").render(
#             **self.content, correlation_matrix_html=correlation_matrix_html
#         )

class HTMLCorrelationTable(CorrelationTable):
    def render(self) -> str:
        correlation_matrix_html = (
            self.content["correlation_matrix"]
            .style
            .set_table_attributes('class="correlation-table table table-striped"')
            .format("{:.3f}")
            .set_properties(**{'text-align': 'center'})  # td 居中
            .set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'center')]}  # th 居中
            ])
            .to_html()
        )
        return templates.template("correlation_table.html").render(
            **self.content, correlation_matrix_html=correlation_matrix_html
        )
