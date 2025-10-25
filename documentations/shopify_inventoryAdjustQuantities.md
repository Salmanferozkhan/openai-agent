# inventoryAdjustQuantities GraphQL Mutation

## Overview
The `inventoryAdjustQuantities` is a GraphQL mutation for adjusting inventory quantities in Shopify's Admin API.

## Authorization Requirements
- Requires `write_inventory` access scope
- User must have permission to apply inventory quantity changes

## Mutation Input
### InventoryAdjustQuantitiesInput
- `reason`: Reason for inventory adjustment (e.g., "correction")
- `name`: Inventory type being adjusted (e.g., "available")
- `referenceDocumentUri`: Optional URI for tracking the adjustment
- `changes`: Array of inventory changes, each containing:
  - `delta`: Quantity change (positive or negative)
  - `inventoryItemId`: Specific inventory item's global ID
  - `locationId`: Location's global ID

## Return Payload
- `inventoryAdjustmentGroup`: Details of the adjustment
  - `createdAt`: Timestamp of adjustment
  - `reason`: Adjustment reason
  - `referenceDocumentUri`: Tracking URI
  - `changes`: List of specific quantity changes
- `userErrors`: List of errors encountered during mutation

## Key Features
- Supports adjusting inventory quantities across different locations
- Provides detailed tracking of inventory modifications
- Includes error handling via `userErrors`

## Example Use Case
Reducing inventory of a specific item by 4 units at a particular warehouse location, with a correction reason and reference document.

## Code Example
```graphql
mutation inventoryAdjustQuantities($input: InventoryAdjustQuantitiesInput!) {
  inventoryAdjustQuantities(input: $input) {
    inventoryAdjustmentGroup {
      createdAt
      reason
      referenceDocumentUri
      changes {
        name
        delta
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

## Example Variables
```json
{
  "input": {
    "reason": "correction",
    "name": "available",
    "changes": [
      {
        "delta": -4,
        "inventoryItemId": "gid://shopify/InventoryItem/123",
        "locationId": "gid://shopify/Location/456"
      }
    ]
  }
}
```

## Supported Programming Languages
- GraphQL
- cURL
- React Router
- Node.js
- Ruby

## API Details
- API Version: 2025-10
- Type: Mutation
- Access: Admin GraphQL API

## Best Practices
- Always provide a reason for inventory adjustments
- Use reference document URIs for tracking and auditing
- Handle potential user errors
- Validate location and inventory item IDs before mutation
