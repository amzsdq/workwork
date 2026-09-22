# B unit 06

If this sample proves useful overlap, the next architecture should retain a single control owner while allowing N read/compute/write workers on partitioned immutable units. Scaling beyond two workers should not be attempted until atomic unit claiming exists, because static partitioning does not establish safety for dynamic queues. The first follow-up should vary spawn offset before increasing worker count.
