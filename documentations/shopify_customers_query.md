# Shopify GraphQL Customers Query

## Overview

The `customers` query in Shopify's GraphQL Admin API allows developers to retrieve and filter customer information from a Shopify store. This query provides comprehensive access to customer data, supporting various filtering, pagination, and sorting options.

## Key Features

- Retrieve detailed customer information
- Filter customers by multiple criteria
- Support for pagination
- Sorting capabilities
- Access to customer account details, contact information, and purchase history

## Query Arguments

### Pagination Arguments
- `first`: Retrieve the first n customers
- `last`: Retrieve the last n customers
- `after`: Cursor for forward pagination
- `before`: Cursor for backward pagination

### Filtering Arguments
- `query`: Advanced filtering with multiple parameters:
  - `country`: Filter by customer's country
  - `email`: Search by email address
  - `first_name`: Filter by first name
  - `last_name`: Filter by last name
  - `state`: Filter by customer account state (ENABLED, DISABLED, etc.)
  - `orders_count`: Filter by number of orders
  - `total_spent`: Filter by total amount spent
  - `tags`: Filter by customer tags
  - `updated_at`: Filter by last update timestamp

### Sorting Arguments
- `sortKey`: Sort results by specific fields
- `reverse`: Reverse the sorting order

## Example Queries

### Retrieve Detailed Customer List
```graphql
query CustomerList {
  customers(first: 50) {
    nodes {
      id
      firstName
      lastName
      defaultEmailAddress {
        emailAddress
      }
      numberOfOrders
      state
    }
  }
}
```

### Filter Customers by Country
```graphql
query {
  customers(first: 5, query: "country:canada") {
    edges {
      node {
        id
        firstName
        lastName
      }
    }
  }
}
```

### Retrieve Enabled Customers
```graphql
query {
  customers(first: 10, query: "state:'ENABLED'") {
    edges {
      node {
        id
        firstName
        lastName
        state
      }
    }
  }
}
```

## Best Practices
- Use pagination for large customer datasets
- Leverage query filters for precise results
- Select only necessary fields to optimize performance
- Handle pagination cursors for efficient data retrieval

## Limitations
- Requires appropriate access scopes
- Query complexity can impact performance
- Some fields may require specific permissions

## API Details
- API Version: 2025-10
- Type: GraphQL Query
- Access: Admin API
