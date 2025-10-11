"""
Example of using ydata-profiling with internationalization
"""
import pandas as pd
from ydata_profiling import ProfileReport
from ydata_profiling.i18n import set_locale
from ydata_profiling.utils.locale_utils import auto_set_locale

# Create sample data
df=pd.DataFrame({
    'bt': [
        '2025-10-10 10:05:00', '2025-10-10 10:10:00','2025-10-10 10:15:00', '2025-10-10 10:20:00',
        '2025-10-10 10:25:00', '2025-10-10 10:30:00', '2025-10-10 10:35:00', '2025-10-10 10:40:00',
        '2025-10-10 10:45:00', '2025-10-10 10:50:00', '2025-10-10 10:55:00', '2025-10-10 11:00:00'
    ],
    '1AL-GG4（一层结算门诊收费办公用电)':[
        54033.6,54033.6,54033.6,54033.6,
        54034.2,54034.2,54034.2,54034.2,
        54034.8,54034.8,54035.4,54035.4
    ],
    '1AL-YF（一层门诊药房办公用电）':[
        300265.2,300266.4,300267.6,300268.8,
        300270,300271.2,300272.4,300273.6,
        300274.8,300276.6,300277.8,300279.1
    ],
    '9AL-ZM4-2#(南楼9层心内三科办公生活用电)':[
        18101.43,18101.43,18101.43,18101.43,
        18101.95,18101.95,18101.95,18101.95,
        18101.95,18101.95,18101.95,18101.95
    ]
})


# Use the default report generation method
print("Default report generation report...")
profile_default = ProfileReport(df, title="Default Data Profiling Report")
profile_default.to_file("default_report.html")

# Auto-detect and set language
print("Auto-detect generation report...")
auto_set_locale()
profile_zh = ProfileReport(df, title="Auto Detect Data Profiling Report")
profile_zh.to_file("auto_report_chinese.html")

# Generate a report in English
print("Generating English report...")
set_locale('en')
profile_en = ProfileReport(df, title="English Data Profiling Report")
profile_en.to_file("report_english.html")

# Generate a report in Chinese
print("Generating Chinese report...")
set_locale('zh')
profile_zh = ProfileReport(df, title="中文数据分析报告")
profile_zh.to_file("report_chinese.html")

# Specify the language during initialization
print("Generating report with locale parameter...")
profile_locale = ProfileReport(df, title="报告标题", locale='zh')
profile_locale.to_file("report_with_locale.html")