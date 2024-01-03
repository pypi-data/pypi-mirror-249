# 当有新的py加入的时候，要在这里更新，__init__.up也要更新

from setuptools import setup ,find_packages

setup(name='macronpy',
      version='1.0.0',
      py_modules=['asset_analysis',
                  'basic_package',
                  'database_connect',
                  'eco_analysis',
                  'macro',
                  'plotly_plot',
                  'port_model',
                  'dbmake',
                  'backtest_multiasset',
                  'backtest_industry',
                  'backtest_fund',
                  'sapo',
                  'srto',
                  'fixincome_analysis',
                  'cms']
  )
# setup(name='macronpy',
#       version='1.0',
#       py_modules= find_packages())
