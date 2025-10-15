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
    '一层办公用电':[
        54033.6,54033.6,54033.6,54033.6,
        54034.2,54034.2,54034.2,54034.2,
        54034.8,54034.8,54035.4,54035.4
    ],
    '二层门办公用电':[
        300265.2,300266.4,300267.6,300268.8,
        300270,300271.2,300272.4,300273.6,
        300274.8,300276.6,300277.8,300279.1
    ],
    '三层办公用电':[
        18101.43,18101.43,18101.43,18101.43,
        18101.95,18101.95,18101.95,18101.95,
        18101.95,18101.95,18101.95,18101.95
    ]
})

# Specify the language during initialization
print("Generating report with locale parameter...")
profile_locale = ProfileReport(df, title="报告标题",
    locale='zh',
    interactions={
        "continuous": True,
        "targets": []
    },
   vars={
        "num": {
            "low_categorical_threshold": 0,  # 设为0，避免数值列被误判为分类
        }
    },
    minimal=False)
profile_locale.to_file("report_with_locale.html")