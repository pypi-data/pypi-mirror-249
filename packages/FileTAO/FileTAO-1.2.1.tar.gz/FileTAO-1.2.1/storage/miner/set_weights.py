# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 philanthrope

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import torch
import wandb
import bittensor as bt


def should_wait_to_set_weights(current_block, last_epoch_block, tempo):
    diff_blocks = current_block - last_epoch_block
    return diff_blocks <= tempo / 2


def set_weights(
    subtensor: "bt.subtensor",
    netuid: int,
    uid: int,
    wallet: "bt.wallet",
    metagraph: "bt.metagraph",
    wandb_on=False,
    tempo=360,
    wait_for_inclusion=False,
    wait_for_finalization=False,
) -> bool:
    """
    Sets the miner's weights on the Bittensor network.

    This function assigns a weight of 1 to the current miner (identified by its UID) and
    a weight of 0 to all other peers in the network. The weights determine the trust level
    the miner assigns to other nodes on the network.

    The function performs the following steps:
    1. Queries the Bittensor network for the total number of peers.
    2. Sets a weight vector with a value of 1 for the current miner and 0 for all other peers.
    3. Updates these weights on the Bittensor network using the `set_weights` method of the subtensor.
    4. Optionally logs the weight-setting operation to Weights & Biases (wandb) for monitoring.

    Args:
        subtensor (bt.subtensor): The Bittensor object managing the blockchain connection.
        netuid (int): The unique identifier for the chain subnet.
        uid (int): The unique identifier for the miner on the network.
        wallet (bt.wallet): The miner's wallet holding cryptographic information.
        metagraph (bt.metagraph): Bittensor metagraph
        wandb_on (bool, optional): Flag to determine if logging to Weights & Biases is enabled. Defaults to False.
        wait_for_inclusion (bool, optional): Wether to wait for the extrinsic to enter a block
        wait_for_finalization (bool, optional): Wether to wait for the extrinsic to be finalized on the chain

    Returns:
        success (bool):
            flag is true if extrinsic was finalized or uncluded in the block.
            If we did not wait for finalization / inclusion, the response is true.

    Raises:
        Exception: If there's an error while setting weights, the exception is logged for diagnosis.
    """
    try:
        # --- query the chain for the most current number of peers on the network
        chain_weights = torch.zeros(subtensor.subnetwork_n(netuid=netuid))
        chain_weights[uid] = 1

        # --- Set weights.
        last_updated = metagraph.last_update[uid].item()
        current_block = subtensor.get_current_block()

        if not should_wait_to_set_weights(current_block, last_updated, tempo):
            success = subtensor.set_weights(
                uids=torch.arange(0, len(chain_weights)),
                netuid=netuid,
                weights=chain_weights,
                wait_for_inclusion=wait_for_inclusion,
                wait_for_finalization=wait_for_finalization,
                wallet=wallet,
                version_key=1,
            )
            if wandb_on:
                wandb.log({"set_weights": 1})
        else:
            bt.logging.info(
                f"Not setting weights because we did it {current_block - last_updated} blocks ago. Last updated: {last_updated}, Current Block: {current_block}"
            )
            success = False

        return success
    except Exception as e:
        if wandb_on:
            wandb.log({"set_weights": 0})
        bt.logging.error(f"Failed to set weights on chain with exception: { e }")
