# Shopify GraphQL Admin API: Fulfillment Query

## Overview
The `fulfillment` query retrieves a Fulfillment resource by its unique ID in the Shopify Admin GraphQL API.

## Access Scopes
Requires one of the following access scopes:
- `read_orders`
- `read_marketplace_orders`
- `read_assigned_fulfillment_orders`
- `read_merchant_managed_fulfillment_orders`
- `read_third_party_fulfillment_orders`
- `read_marketplace_fulfillment_orders`

## Query Arguments
- `id` (ID!, required): The unique identifier of the Fulfillment to retrieve

## Returned Object: Fulfillment
A Fulfillment represents a shipment of one or more items in an order. Key characteristics:
- Can have multiple fulfillments per order
- Represents items sent to a customer
- Provides detailed shipping and tracking information

## Key Returnable Fields
- `fulfillmentLineItems`: Details of items in the fulfillment
- `status`: Current fulfillment status
- `estimatedDeliveryAt`: Projected delivery date
- `location`: Shipping location details
- `service`: Fulfillment service handle
- `trackingInfo`: Shipping tracking details
- `originAddress`: Shipping origin address
- `deliveredAt`: Actual delivery timestamp
- `inTransitAt`: When the fulfillment was in transit
- `displayStatus`: Human-readable fulfillment status

## Example Use Cases
1. Retrieve detailed fulfillment information
2. Track shipping status
3. Get line item details for a specific fulfillment
4. Retrieve fulfillment events

## Code Examples
The documentation provides implementation examples in:
- GraphQL
- cURL
- React Router
- Node.js
- Ruby

## Sample Query
```graphql
query FulfillmentShow($id: ID!) {
  fulfillment(id: $id) {
    fulfillmentLineItems(first: 10) {
      edges {
        node {
          id
          lineItem {
            title
            variant {
              id
            }
          }
        }
      }
    }
    status
    trackingInfo(first: 10) {
      company
      number
      url
    }
  }
}
```

## Best Practices
- Use appropriate access scopes for your use case
- Handle pagination for fulfillment line items
- Retrieve only the fields you need
- Check fulfillment status before performing operations
- Utilize tracking information for customer communication

## Common Use Cases
1. Display fulfillment details to customers
2. Track shipment status
3. Retrieve line items in a fulfillment
4. Get tracking information for customer service
5. Monitor delivery status
6. Manage multi-fulfillment orders

## API Details
- API Version: 2025-10
- Type: GraphQL Query
- Access: Admin API
