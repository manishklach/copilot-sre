# Payments Dependency Outage

1. Confirm whether the failing endpoint changed in the latest deploy.
2. Compare checkout and payments service configuration for endpoint, DNS, and retry settings.
3. Check whether circuit breakers opened and whether fallback behavior is active.
4. If customer impact remains high, roll back the most recent dependent deploy first.
