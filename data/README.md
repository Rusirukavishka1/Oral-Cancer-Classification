# Data and saved results

The original dataset is intentionally not included in this GitHub upload bundle. Its source URL and redistribution license were not supplied. No license is asserted for it.

For local use, copy your existing `oral_cancer_prediction_dataset.csv` into this directory. The file is ignored by Git. Expected SHA256:

`3070535bfa747261a97901018a6c9391ac97356cba1c4fd9dd63c99e5f15763b`

The app validates this fingerprint before displaying metrics. A different CSV requires a new matched evaluation bundle, not merely a new hash.

Included files:
- `model_summary.csv`: pooled out-of-fold scores from saved notebook tables.
- `fold_results.csv`: 48 model/fold metric rows.
- `reports.txt`: pooled classification reports, UTF-8 encoded.
- `provenance.json`: source fingerprints and runtime details.

Saved results and notebook figures are derived from the supplied dataset. Confirm source terms before making the repository public. Document the dataset URL, creator, version, license and collection process when available.
