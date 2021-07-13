# !/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk.future.transaction import PaymentTxn
from algosdk import account

# Connect to Algorand node maintained by PureStake
# Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
# algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
    "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000  # https://developer.algorand.org/docs/features/accounts/#minimum-balance

# generate an account
private_key, account_address = account.generate_account()
mnemonic_phrase = mnemonic.from_private_key(private_key)
print("My account_address: {}".format(account_address))
print(mnemonic_phrase)

def send_tokens(receiver_pk, tx_amount):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    sender_address = "A6WMB5K7WINZ4SU2U33K2XBSKR6YUIBFKVKDNCV5J4OASR54K6MSZSIOJ4"
    phrase = "inform lake track love vacuum juice virtual main define planet subway casual talent flip joke argue " \
             "robust student above fat palace carpet mandate abstract neck"

    # construct the transaction
    unsigned_txn = transaction.PaymentTxn(sender_address, tx_fee, first_valid_round, last_valid_round, gen_hash,
                                          receiver_pk, tx_amount)
    print("Created Txn")
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(phrase))
    print("Signed Txn")
    txid = acl.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    return sender_address, txid


# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo
