# MCA_Project

This repository hosts an experimental implementation of **ExpenseIQ**, a smart
personal expense and budget advisor. The first step of the methodology focuses
on ingesting PDF bank statements and normalising them into a common schema for
subsequent analysis.

## Current features

- `expenseiq.ingestion` provides helper functions to detect the issuing bank
  from a PDF statement and convert transaction tables into a standard format.
  The current implementation includes column mappings for **SBI**, **HDFC** and
  **ICICI** statements.
- Basic unit tests covering bank detection and column normalisation.

Future work will expand the pipeline with categorisation, dashboards and other
analytics.
