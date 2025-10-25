# GraphQL Order Query

## Overview

The `order` query retrieves an order by its ID, providing comprehensive order information such as:
- Customer details
- Line items
- Financial data
- Fulfillment status

## Query Signature

```graphql
query {
  order(id: ID!): Order
}
```

### Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `ID!` | Yes | The unique identifier of the order to retrieve |

## Use Cases

The `order` query is useful for:
- Order management and fulfillment
- Financial reporting
- Customer purchase history
- Transaction analysis
- Shipping and inventory management

## Important Limitations

- By default, only the last 60 days of orders are retrievable
- To access older orders, you must [request access to all orders](https://shopify.dev/docs/api/usage/access-scopes#orders-permissions)

## Recommended Practices

For large order datasets, Shopify recommends using [bulk operations](https://shopify.dev/docs/api/usage/bulk-operations/queries), which:
- Handle pagination automatically
- Allow asynchronous data retrieval
- Avoid API rate limit constraints

## Example Query

```graphql
query {
  order(id: "gid://shopify/Order/148977776") {
    id
    name
    totalPriceSet {
      presentmentMoney {
        amount
      }
    }
    lineItems(first: 10) {
      nodes {
        id
        name
      }
    }
  }
}
```

## Related Resources

- [Creating orders](https://shopify.dev/docs/api/admin-graphql/latest/mutations/ordercreate)
- [Order management apps](https://shopify.dev/docs/apps/build/orders-fulfillment)

## API Version

- Current version: 2025-10
