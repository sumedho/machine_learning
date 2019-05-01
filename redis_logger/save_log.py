import redis
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

r = redis.Redis()

def calc_subblock_times(subs):
    sub = subs.subblock.values
    pred = subs.prediction.values

    c = np.empty((sub.size + pred.size,), dtype=sub.dtype)
    c[0::2] = pred
    c[1::2] = sub

    diff_time = np.diff(c)

    ptimes = diff_time[0::2]
    stimes = diff_time[1::2]
    stimes = np.insert(stimes,0,0)

    return pd.DataFrame({'nblocks':subs.nblocks,'pred_time':ptimes, 'sub_time':stimes})

def calc_ops(ops):
    elapsed_time = ops.datetime.diff()[1:].values
    op_name = ops.op[:-1].values

    return pd.DataFrame({'name':op_name,'time':elapsed_time})

def parse_logging(redis_conn):
    logged_times = []
    logged_ops = []
    logged_subblocking = []
    logged_predict = []
    logged_nblocks = []

    op_times = redis_conn.lrange('TESTDATA', 0, -1)
    op_names = redis_conn.lrange('TESTDATA:OPERATION', 0, -1)
    sb_times = redis_conn.lrange('SUBBLOCK', 0, -1)
    pred_times = redis_conn.lrange('SUBPREDICT', 0, -1)
    blocks = redis_conn.lrange('nblocks', 0, -1)

    for t in op_times:
        logged_times.append(float(t))
        #logged_times.append(datetime.fromtimestamp(float(t)))

    for op in op_names:
        logged_ops.append(op.decode('ascii'))

    for t in sb_times:
        #logged_subblocking.append(datetime.fromtimestamp(float(t)))
        logged_subblocking.append(float(t))

    for t in pred_times:
        #logged_predict.append(datetime.fromtimestamp(float(t)))
        logged_predict.append(float(t))

    for n in blocks:
        logged_nblocks.append(int(n))

    ops = pd.DataFrame({'op':logged_ops,'datetime':logged_times})
    subblocking = pd.DataFrame({'subblock':logged_subblocking, 'prediction':logged_predict, 'nblocks':logged_nblocks})

    return ops, subblocking


ops, subs = parse_logging(r)

ops_result = calc_ops(ops)
sub_result = calc_subblock_times(subs)

ops_result['pct_time'] =  np.round((ops_result.time/ops_result.time.sum())*100, 1)

ops_result.to_csv('operation_times.csv', index=False)
sub_result.to_csv('subblock_times.csv', index=False)

plt.figure(figsize=(12,10))
plt.plot(sub_result.sub_time, label='subblocks')
plt.plot(sub_result.pred_time, label='predictions')
plt.legend()
plt.xlabel('Level number')
plt.ylabel('Time (s)')

total_time = sub_result.sub_time.sum() + sub_result.pred_time.sum()
pct_stime = np.round(sub_result.sub_time.sum()/total_time*100,1)
pct_ptime = np.round(sub_result.pred_time.sum()/total_time*100,1)
plt.title('Blocks: {0:,} \nSub time (%): {1}\n Pred time (%): {2}'.format(sub_result.nblocks.sum(), pct_stime, pct_ptime))
plt.savefig('subblock_times.png')
