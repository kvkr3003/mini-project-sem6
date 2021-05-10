from client_api import NetCacheClient

import numpy as np
import time




def main(n_servers, disable_cache, suppress, input_files):
    client = NetCacheClient(n_servers=n_servers, no_cache=disable_cache)

    curr_latency= 0.1
    prev_latency= 0.1

    for filepath in input_files:
        sample = []

        with open(filepath) as fp:
            line = fp.readline()
            while line:
                sample.append(line.strip())
                line = fp.readline()

        hot_threshold=0

        for query in sample:
            # hot_threshold= hot_threshold + 1
            # start_time= time.time()
            client.read(query, suppress=suppress)
            # latency= time.time()-start_time
            # curr_latency= latency
            # print(curr_latency,prev_latency)
            # if curr_latency > 10*prev_latency:
            #     print("this is the hot parameter",hot_threshold)
            #     break
            # prev_latency= curr_latency


        #print("\n########## SERVER METRICS REPORT ##########")
        #print("########## [{}] ##########\n".format(filepath))

        if disable_cache:
            x = 'nocache'
        else:
            x = 'netcache'

        input_file = filepath.split('/')[1].split('.')[0]

        out_file = 'results/{}_{}_{}.txt'.format(input_file, n_servers, x)
        out_fd = open(out_file, 'w')

        client.request_metrics_report(output=out_fd)


if __name__=="__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--n-servers', help='number of servers', type=int, required=False, default=1)
    parser.add_argument('--disable-cache', help='disable in-network caching', action='store_true')
    parser.add_argument('--suppress', help='suppress output', action='store_true')
    parser.add_argument('--input', help='input files to execute queries', required=True, nargs="+")
    args = parser.parse_args()

    main(args.n_servers, args.disable_cache, args.suppress, args.input)
