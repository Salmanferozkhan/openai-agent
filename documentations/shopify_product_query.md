# Shopify GraphQL Admin API: Product Query

## Overview

The `product` query retrieves a specific product by its ID in the Shopify Admin GraphQL API. It allows developers to access comprehensive product information and perform various operations.

## Key Features

- Retrieve detailed product information
- Access product metadata
- Manage product variants
- Handle international sales and localization
- Retrieve product media and images

## Query Arguments

| Argument | Type | Description | Required |
|----------|------|-------------|----------|
| `id` | `ID!` | The unique identifier of the product to retrieve | Yes |

## Possible Return Fields

- `id`: Product's unique identifier
- `title`: Product name
- `description`: Product description
- `variants`: Product variant details
- `collections`: Collections the product belongs to
- `media`: Product images and videos
- `metafields`: Custom metadata associated with the product
- `totalInventory`: Total inventory count
- `onlineStoreUrl`: Product's online store URL

## Use Cases

1. Build product detail pages
2. Manage inventory
3. Handle international sales
4. Retrieve product media
5. Access product metadata
6. Manage product variants
7. Retrieve localized product information

## Example Query

```graphql
query {
  product(id: "gid://shopify/Product/108828309") {
    title
    description
    totalInventory
  }
}
```

## Important Considerations

- Requires appropriate access scopes
- Supports pagination for large result sets
- Provides flexible querying of product information
- Supports multilingual and market-specific translations

## Supported Languages/Platforms

- GraphQL
- JavaScript (React, Node.js)
- Ruby
- cURL

## Best Practices

- Use specific field selection
- Implement pagination for large datasets
- Handle potential null values
- Use variables for dynamic queries
