import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
# 大单同步表
BIG_DEAL_NAME = "ths_big_deal_fund"
# 大单选择表
BIG_DEAL_CHOOSE_NAME = "big_deal_fund_choose"
# 实时行情表
REAL_TIME_QUOTES_NOW = 'realtime_quotes_now'
# 当前实时涨停表
TODAY_ZT_POOL = 'today_zt_pool'
# 集合竞价表
CALL_AUCTION_DB_NAME = 'call_auction_signal'
# 实时竞价表
CALL_AUCTION_DB_NAME_REAL_TIME = 'call_auction_signal_realtime'
# 涨停打板表
NOW_TIME_ZT_DA_BAN = 'now_time_zt_da_ban'
