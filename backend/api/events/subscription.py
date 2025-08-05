from blinker import signal

subscription_was_created = signal('subscription-was-created')

transaction_was_created = signal('transaction-was-created')

transaction_is_paying = signal("transaction-is-paying")

transaction_was_paied = signal("transaction-was-paid")

transaction_was_cancelled = signal("transaction-was-cancelled")

transaction_was_refunded = signal("transaction-was-refunded")
