# orderCreate Mutation

## Overview

The `orderCreate` mutation allows programmatically generating orders in Shopify, particularly useful for scenarios outside the standard checkout process such as:
- Importing orders from external systems
- Creating orders for wholesale customers

## Key Characteristics

### Access and Permissions
- Requires `write_orders` access scope
- Only accessible to apps with offline access tokens
- Limited to 5 new orders per minute in trial/development stores

### Limitations
- Doesn't support applying multiple discounts
- Automatic discounts won't be applied automatically
- Only one discount code can be set per order

## Mutation Arguments

### `order` (Required)
Type: `OrderCreateOrderInput!`
Attributes for creating a new order, including:
- Line items
- Customer information
- Shipping/billing addresses
- Transactions
- Taxes
- Discounts

### `options` (Optional)
Type: `OrderCreateOptionsInput`
Strategies for:
- Inventory updates
- Sending shipping confirmations
- Sending order receipts

## Subsequent Order Editing

After creating an order, you can modify it using:

1. `orderUpdate` mutation
   - Simple updates like changing notes, tags, customer info

2. `orderEditBegin` mutation
   - Significant updates such as:
     - Adding/removing line items
     - Changing quantities
     - Modifying discounts

## Example Use Cases

- Create orders with custom pricing
- Apply single discount codes
- Handle multi-currency transactions
- Create orders with tax lines
- Manage fulfillment details
- Control email notification settings

## Code Example (JavaScript)

```javascript
mutation orderCreate($order: OrderCreateOrderInput!, $options: OrderCreateOptionsInput) {
  orderCreate(order: $order, options: $options) {
    userErrors {
      field
      message
    }
    order {
      id
      // Selected order details
    }
  }
}
```

## Best Practices

- Validate input data thoroughly
- Handle potential user errors
- Respect rate limits
- Use appropriate access tokens
- Consider currency and tax implications
