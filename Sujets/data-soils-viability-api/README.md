
# Data certification API

Le Wagon Data Science certification exam starter pack for the predictive API test.

**💡&nbsp;&nbsp;This challenge is completely independent of other challenges. It is not required to complete any other challenge in order to work on this challenge.**

## API challenge

**📝&nbsp;&nbsp;In this challenge, you are provided with a trained model saved as `assets/model.joblib`. The goal is to create an API that will predict the viability of a soil based on analysis results.**

👉&nbsp;&nbsp;You will only need to edit the code of the API in `api/fast.py` 🚨

👉&nbsp;&nbsp;The package versions listed in `requirements.txt` should work out of the box with the pipelined model saved in `assets/model.joblib`

### Install the required packages

The `requirements.txt` file lists the exact version of the packages required in order to be able to load the pipelined model that we provide.

``` bash
pip install -r requirements.txt
```

### Run a uvicorn server

**📝&nbsp;&nbsp;Start a `uvicorn` server in order to make sure that the setup works correctly.**

Run the server:

```bash
uvicorn api.fast:app --reload
```

Open your browser at http://localhost:8000/

👉&nbsp;&nbsp;You should see the response `{"Status": "Up and running"}`

You will now be able to work on the content of the API while `uvicorn` automatically reloads your code as it changes.

### API specification

**Predict the viability of a soil**

`GET /predict`

| Parameter | Type | Description |
|---|---|---|
| measure_index | float | Engineered measure of soil characteristics |
| measure_moisture | float | Moisture level of the soil  |
| measure_temperature | float | Temperature of the soil, in Celsius degrees |
| measure_chemicals | float | Indice of chemicals presence in the soil |
| measure_biodiversity | float | Indice of biodiversity in the soil  |
| main_element | string | Symbol of the main chemical element found in the soil |
| soil_condition | string | Overall indicator of the soil fertility |
| datetime_start | string | Timestamp of experiment's start  |
| datetime_end | string | Timestamp of experiment's end |

Returns a dictionary containing the viability of the soil in the `viable` key, as a `boolean`.

Example request:

```
/predict?measure_index=55.79&measure_moisture=28.74&measure_temperature=20.3&measure_chemicals=1.13&measure_biodiversity=437.36&main_element=K&soil_condition=normal&datetime_start=2018-10-12+15%3A14%3A58&datetime_end=2018-10-12+17%3A58%3A38
```

Example response:

``` json
{
  "viable": true
}
```

👉 It is your turn, code the endpoint in `api/fast.py`. If you want to verify what data types the pipeline expects, have a look at the API specifications above.

## API in production

**📝&nbsp;&nbsp;Push your API to production on the hosting service of your choice.**

<details>
  <summary>👉&nbsp;&nbsp;If you opt for Google Cloud Platform 👈</summary>

  &nbsp;


Once you have changed your `GCP_PROJECT_ID` in the `Makefile`, run the directives of the `Makefile` to build and deploy your containerized API to Container Registry and finally Cloud Run.

</details>
