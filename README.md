\# E-commerce API Extractor



\## Description



This project uses Python and HTTP GET requests to retrieve product data from a REST API and save it locally as a JSON file.



It also practices query parameters, pagination, HTTP status codes, error handling, Python virtual environments, and Git for version control.



\## Data Source



The project uses the DummyJSON API:



https://dummyjson.com/products



The API contains dummy e-commerce product data.



\## How It Works



First, the program sends an HTTP GET request to the API using Python's `requests` library.



The API returns product data in JSON format. By default, the response only contains part of the complete dataset, so pagination is required to retrieve all 194 products.



For this project, each request retrieves 10 products. A loop changes the `skip` parameter after every request so that the following request retrieves the next group of products.



Each group of products is added to the `all\_products` list using `extend()`.



The loop stops once the number of records requested reaches or exceeds the total number of products available.



The script also includes error handling so HTTP/request errors can be caught and displayed instead of causing an unhandled program error.



Finally, all retrieved products are saved locally as a readable JSON file.



\## Pagination



The API supports the query parameters `limit` and `skip`.



`limit` controls how many products are returned in each request.



For example:



\- `limit=10\&skip=0` returns products 1–10.

\- `limit=10\&skip=10` returns products 11–20.

\- `limit=10\&skip=20` returns products 21–30.



`skip` determines how many existing records should be ignored before the API starts returning data.



The program increases `skip` by the value of `limit` after every successful request.



The loop stops when:



`skip + limit >= total`



\## Error Handling



The script uses `response.raise\_for\_status()` to detect HTTP errors such as 404 or 500 responses.



The request is placed inside a `try` block, and request-related errors are caught using `requests.RequestException`.



If an error occurs, the script prints information about the error and stops the pagination loop gracefully instead of crashing with an unhandled exception.



A timeout is also included so the program does not wait indefinitely for an API response.



\## Output



The extracted product data is saved as:



`data/raw/products.json`



The JSON is formatted with indentation so that it is easy to read.



\## How to Run



Activate the project's virtual environment and run:



`python src\\extract.py`



\## What I Learned



Through this project I practiced:



\- HTTP GET requests

\- REST APIs and endpoints

\- HTTP status codes

\- Query parameters

\- JSON responses

\- Offset-based pagination using `limit` and `skip`

\- API error handling

\- Python's `requests` library

\- Saving JSON data locally

\- Python virtual environments

\- Git version control and commits

