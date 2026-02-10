from evidence_destroy.core import SecureWiper
w=SecureWiper(passes=3,method="random_fill")
print(f"Wipe method: {w.method}")
print(f"Passes: {w.passes}")
print("Running in DRY RUN mode - no files will be destroyed")
