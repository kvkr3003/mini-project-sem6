#include <core.p4>
#include <v1model.p4>

#include "../include/headers.p4"

#define CONTROLLER_MIRROR_SESSION 100

#define HOT_KEY_THRESHOLD 3

#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4
#define PKT_INSTANCE_TYPE_REPLICATION 5
#define PKT_INSTANCE_TYPE_RESUBMIT 6

#define pkt_is_mirrored \
	((standard_metadata.instance_type != PKT_INSTANCE_TYPE_NORMAL) && \
	 (standard_metadata.instance_type != PKT_INSTANCE_TYPE_REPLICATION))

#define pkt_is_not_mirrored \
	 ((standard_metadata.instance_type == PKT_INSTANCE_TYPE_NORMAL) || \
	  (standard_metadata.instance_type == PKT_INSTANCE_TYPE_REPLICATION))


control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

	#include "query_statistics.p4"

	// per-key counter to keep query frequency of each cached item
	counter((bit<32>) NETCACHE_ENTRIES * NETCACHE_VTABLE_NUM, CounterType.packets) query_freq_cnt;
	register<bit<32>>(10) count_query;

    apply {

		if (hdr.netcache.isValid()) {

			// if the bitmap is not full of zeros then we had cache hit

			bool cache_hit = (meta.vt_bitmap != 0);

			bit<32> t1;
			count_query.read(t1, 0);
			t1=t1+1;
			count_query.write(0, t1);	
			
			if (hdr.netcache.op == READ_QUERY) {

				bit<32> t2;
				count_query.read(t2, 1);
				t2=t2+1;
				count_query.write(1, t2);	


				if (!cache_hit) 
				{
					bit<32> t3;
					count_query.read(t3, 2);
					t3=t3+1;
					count_query.write(2, t3);	

					// waiting for the answer of the KV store allows us to
					// retrieve the actual key-value pair from the reply
					if (pkt_is_not_mirrored && hdr.udp.srcPort != NETCACHE_PORT) {

						update_count_min_sketch();
						if (meta.key_cnt >= HOT_KEY_THRESHOLD) 
						{
							bit<32> t4;
							count_query.read(t4, 3);
							t4=t4+1;
							count_query.write(3, t4);

							inspect_bloom_filter();
							if (meta.hot_query == 1) {
								update_bloom_filter();
								
								bit<32> t5;
								count_query.read(t5, 4);
								t5=t5+1;
								count_query.write(4, t5);

								// inform the server that he will receive a read query
								// for a hot key (this is needed, so he will block until
								// the insertion in cache is completed) - cache coherence
								hdr.netcache.op = HOT_READ_QUERY;

								//clone(CloneType.E2E, CONTROLLER_MIRROR_SESSION);
							}
						}
					}

				} else 
				{
					//cache hit
					// update query frequency counter for cached item
					bit<32> t6;
					count_query.read(t6, 5);
					t6=t6+1;
					count_query.write(5, t6);

					query_freq_cnt.count((bit<32>) meta.key_idx);
				}



			// if the server informs us that the delete operation on the key completed
			// successfully then we forward this packet to the controller to update the
			// cache and validate the key again
			} else if (hdr.netcache.op == DELETE_COMPLETE && cache_hit) {

				if (pkt_is_not_mirrored && hdr.tcp.srcPort == NETCACHE_PORT) {
					clone(CloneType.E2E, CONTROLLER_MIRROR_SESSION);
				}

			}

		}

	}

}
