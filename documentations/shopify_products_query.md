# Shopify GraphQL Products Query Documentation

## Overview

The `products` query in Shopify's GraphQL Admin API allows developers to retrieve a list of products from a store with extensive filtering and pagination capabilities.

## Key Use Cases

- Build product catalog browsing interfaces
- Create product searching and sorting experiences
- Implement product recommendations
- Sync product data with external systems

## Query Capabilities

### Supported Features
- Pagination for large product catalogs
- Saved searches for frequently used queries
- Comprehensive product metadata retrieval

### Retrievable Product Metadata
- Basic product information (title, description, vendor)
- Product options and variants
- Pricing and inventory details
- Media attachments
- SEO metadata
- Product categories and tags
- Availability and publishing statuses

## Query Arguments

### Pagination Arguments
- `after`: Cursor for pagination
- `before`: Cursor for pagination
- `first`: Number of initial results
- `last`: Number of final results

### Filtering Arguments
- `query`: Advanced search and filtering
- `reverse`: Reverse result order
- `savedSearchId`: Use predefined saved search
- `sortKey`: Define sorting method

## Query Examples

### Basic Product Retrieval
```graphql
query {
  products(first: 10) {
    nodes {
      id
      title
    }
  }
}
```

### Filtered Product Search
```graphql
query {
  products(first: 10, query: "product_type:snowboards") {
    edges {
      node {
        title
      }
    }
  }
}
```

## Best Practices
- Use pagination for large datasets
- Leverage query filters for precise results
- Utilize fragments for complex queries
- Consider performance when designing queries

## Limitations
- Requires appropriate access scopes
- Query complexity can impact performance
- Some fields may require specific permissions

## API Details
- API Version: 2025-10
- Type: GraphQL Query
- Access: Admin API
