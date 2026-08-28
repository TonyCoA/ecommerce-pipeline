# E-commerce Data Pipeline

## Description

This project builds a small end-to-end data pipeline using Python, a REST API, JSON, PostgreSQL, and Git.

The pipeline extracts product data from DummyJSON, saves the raw API response locally, validates the data, loads it into a relational PostgreSQL database, and allows the data to be queried using SQL and Python.

## Data Source

The project uses the DummyJSON products API:

https://dummyjson.com/products

The source contains dummy e-commerce product data, including product information, reviews, images, metadata, stock, prices, ratings, and other attributes.

## Pipeline Overview

```text
DummyJSON API
      ↓
HTTP GET requests
      ↓
Pagination
      ↓
Raw JSON
      ↓
Source validation
      ↓
Python + Psycopg
      ↓
PostgreSQL
      ↓
Relational tables
      ↓
SQL / Python queries