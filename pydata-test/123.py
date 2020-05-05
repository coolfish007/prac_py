import pandas as pd
import numpy as np
from openpyxl import load_workbook

product_df = pd.DataFrame({
    'id':
    np.arange(101, 111),
    'date':
    pd.date_range(start='20200505', periods=10),
    'money': [5, 4, 65, 10, 15, 20, 35, 16, 6, 20],
    'product':
    ['苏打水', '可乐', '牛肉干', '老干妈', '菠萝', '冰激凌', '洗面奶', '洋葱', '牙膏', '薯片'],
    'department':
    ['饮料', '饮料', '零食', '调味品', '水果', np.nan, '日用品', '蔬菜', '日用品', '零食'],
    'origin': [
        'China', ' China', 'America', 'China', 'Thailand', 'China', 'america',
        'China', 'China', 'Japan'
    ]
})

product_df
