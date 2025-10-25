# fulfillmentCancel GraphQL Mutation

## Overview
The `fulfillmentCancel` mutation allows cancellation of a specific fulfillment in the Shopify Admin GraphQL API.

## Mutation Details
- **API Version**: 2025-10
- **Type**: Mutation
- **Purpose**: Cancel a specific fulfillment

## Arguments
- `id` (ID!, Required)
  - Unique identifier of the fulfillment to be canceled
  - Must be a valid Shopify Fulfillment Global ID

## Return Payload
1. `fulfillment` (Fulfillment)
   - Returns the canceled fulfillment object
   - Includes updated status and ID

2. `userErrors` ([UserError!]!)
   - List of potential errors encountered during cancellation
   - Each error contains:
     - `field`: Specific field causing the error
     - `message`: Detailed error description

## Example Usage
Multiple language implementations are provided, including:
- GraphQL
- cURL
- React Router
- Node.js
- Ruby

### Sample GraphQL Mutation
```graphql
mutation fulfillmentCancel($id: ID!) {
  fulfillmentCancel(id: $id) {
    fulfillment {
      id
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

### Sample Variables
```json
{
  "id": "gid://shopify/Fulfillment/237894043"
}
```

## Typical Response
```json
{
  "fulfillmentCancel": {
    "fulfillment": {
      "id": "gid://shopify/Fulfillment/237894043",
      "status": "CANCELLED"
    },
    "userErrors": []
  }
}
```

## Key Considerations
- Requires a valid fulfillment ID
- Successful cancellation changes fulfillment status to "CANCELLED"
- Returns any potential user errors during the process

## Access Requirements
- Requires appropriate fulfillment access scopes
- User must have permission to cancel fulfillments

## Best Practices
- Always validate the fulfillment ID before cancellation
- Handle user errors appropriately
- Check fulfillment status before attempting cancellation
- Verify that the fulfillment can be canceled

## Common Use Cases
1. Cancel incorrect fulfillments
2. Handle order changes requiring fulfillment cancellation
3. Manage fulfillment errors
4. Update order status after fulfillment issues
