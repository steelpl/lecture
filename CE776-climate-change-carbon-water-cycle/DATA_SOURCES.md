# Data sources and scope

| Data | Use and coverage | Source |
|---|---|---|
| SRTM 30 m | Elevation (m) based on observations in 2000; metadata and regional means | [NASA/USGS/JPL](https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003) |
| Landsat 8 C2 L2 | Reflectance in 2020; scale, offset and QA | [USGS](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) |
| Sentinel-2 SR Harmonized | Reflectance, NDVI, MNDWI and classification in 2020 | [Copernicus](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED) |
| CHIRPS v2 Final Daily | Daily precipitation in 2020; mm/day, 0.05° | [UCSB CHG](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY) |
| WorldCover v100 | Categorical map for 2020, 10 m; ESA WorldCover Consortium, CC BY 4.0 | [ESA](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100) |
| JRC Global Surface Water 1.4 | Water occurrence (%) over 1984–2021; not present-day ground truth | [EC JRC](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater) |
| Monte Carlo, ANOVA, quantile regression and data merging | Instructor-provided examples; 102 positive precipitation observations from 2023; TC includes synthetic truth | Guide sheet in each workbook |

The precipitation–temperature file does not identify its station or detailed collection method. Do not infer missing metadata. Verify the original metadata before drawing regional climate conclusions beyond this teaching example.

GEE queries the public catalog; raw satellite products are not copied into this repository. Check each product's citation and use conditions before using it in research.

Source PPTX files, PDFs, lecture videos and full research papers are not published here. The GEE activities retain public-data processing that supports the learning goals. They do not include personal assets, automatic storage or an unvalidated flood-analysis pipeline.

References for physical and statistical explanations: [FAO evapotranspiration concepts](https://www.fao.org/4/x0490e/x0490e04.htm), [GCOS Essential Climate Variables](https://gcos.wmo.int/site/global-climate-observing-system-gcos/essential-climate-variables), [Vecellio et al., 2022](https://doi.org/10.1152/japplphysiol.00738.2021), [ASA statement on p-values](https://doi.org/10.1080/00031305.2016.1154108).
