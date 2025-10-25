# fulfillmentCreate GraphQL Mutation

## Overview
The `fulfillmentCreate` mutation allows creating a fulfillment for one or multiple fulfillment orders associated with the same order and assigned to the same location.

## Access Requirements
- Required access scopes:
  - `write_assigned_fulfillment_orders`
  - `write_merchant_managed_fulfillment_orders`
  - `write_third_party_fulfillment_orders`
- User must have "fulfill_and_ship_orders" permission

## Mutation Arguments

### fulfillment (Required)
- Type: `FulfillmentInput!`
- Description: Input fields for creating a fulfillment from fulfillment orders

### message (Optional)
- Type: `String`
- Description: Optional message for the fulfillment request

## Payload Returns

### fulfillment
- Type: `Fulfillment`
- Description: The created fulfillment

### userErrors
- Type: `[UserError!]!`
- Description: List of errors encountered during mutation execution

## Input Structure Example
```json
{
  "fulfillment": {
    "trackingInfo": {
      "number": "<tracking-number>",
      "url": "https://example.myshopify.com",
      "company": "<shipping-company>"
    },
    "notifyCustomer": true,
    "lineItemsByFulfillmentOrder": [
      {
        "fulfillmentOrderId": "gid://shopify/<objectName>/10079785100",
        "fulfillmentOrderLineItems": [{}]
      }
    ],
    "originAddress": {
      "address1": "<street-address>",
      "city": "<city>",
      "countryCode": "<country-code>"
    }
  },
  "message": "<optional-message>"
}
```

## GraphQL Mutation Template
```graphql
mutation fulfillmentCreate($fulfillment: FulfillmentInput!, $message: String) {
  fulfillmentCreate(fulfillment: $fulfillment, message: $message) {
    fulfillment {
      id
      status
      trackingInfo {
        number
        url
        company
      }
      location {
        name
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

## Key Features
- Create fulfillments for multiple fulfillment orders
- Support for tracking information
- Customer notification options
- Origin address specification
- Error handling through userErrors

## Best Practices
- Ensure all fulfillment orders are from the same order
- Verify all fulfillment orders are assigned to the same location
- Include tracking information for customer communication
- Handle potential user errors appropriately
- Use appropriate access scopes based on fulfillment type

## Common Use Cases
1. Create fulfillment with tracking information
2. Fulfill orders from specific locations
3. Notify customers of shipment
4. Track fulfillment status
5. Manage multi-location fulfillments

## API Details
- API Version: 2025-10
- Type: Mutation
- Access: Admin GraphQL API
