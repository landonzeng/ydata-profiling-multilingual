from ydata_profiling.report.presentation.core.sample import Sample
from ydata_profiling.report.presentation.flavours.html import templates


# class HTMLSample(Sample):
#     def render(self) -> str:
#         sample_html = self.content["sample"].to_html(
#             classes="sample table table-striped",
#             justify = 'left'
#         )
#         return templates.template("sample.html").render(
#             **self.content, sample_html=sample_html
#         )

class HTMLSample(Sample):
    def render(self) -> str:
        sample_html = (
            self.content["sample"]
            .style
            .set_table_attributes('class="sample table table-striped"')
            .set_table_styles([
                {'selector': 'th', 'props': [('text-align', 'center')]},  # 所有 th 居左
                {'selector': 'td', 'props': [('text-align', 'center')]}
            ])
            .to_html()
        )
        return templates.template("sample.html").render(
            **self.content, sample_html=sample_html
        )