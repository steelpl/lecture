# Earth Engine setup

The GEE activities develop an understanding of satellite-data units, spatial and temporal processing, and interpretation. Follow inputs → processing → outputs rather than memorizing entire programs.

1. Review the [Earth Engine access guide](https://developers.google.com/earth-engine/guides/access) using your Google account.
2. Check your own or your institution's Google Cloud project. Earth Engine registration, an enabled API and account permissions are required.
3. Enter the registered project **ID** in the notebook's `PROJECT_ID` field.
4. Use a CPU runtime. Run installation → authentication → processing → queries → map cells in order.

Noncommercial access also has eligibility requirements and quotas. Check the [official guidance](https://developers.google.com/earth-engine/guides/noncommercial_tiers) for current access, pricing and quota conditions. Authentication and Cloud project registration are separate steps.

Colab resources and session limits may vary. A GPU is unnecessary for these activities. See the [Colab FAQ](https://research.google.com/colaboratory/faq.html).

| Issue | Check |
|---|---|
| Invalid project ID | Use the project ID, not its display name. |
| Permission or registration error | Check the signed-in account, EE registration, API and permissions. |
| Empty image collection | Check the region, period, cloud filters and `collection.size()`. |
| Slow map | Check the computation region and scale; start with a small area. |
| Oversized query | Request small summary statistics instead of calling `getInfo()` on an entire image. |

The notebooks do not automatically mount a personal Drive, save EE assets or export data. Server objects describe computations; `getInfo()` and map display trigger requests.

The years 2000, 2020 and 2023 identify fixed observation examples. Do not replace them when the teaching year changes.
