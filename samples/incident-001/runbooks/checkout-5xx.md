# Checkout 5xx Triage

1. Check whether any deploy happened within 15 minutes of first alert.
2. Compare runtime environment variables with the last known healthy release.
3. Validate payment-provider connectivity from the checkout service.
4. Roll back if customer impact remains high and mitigation is not immediately available.
