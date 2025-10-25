# inventoryLevel GraphQL Query

## Overview
The `inventoryLevel` query returns an [InventoryLevel](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel) object by its unique ID, providing detailed inventory information for a specific item at a particular location.

## Query Arguments
- `id` (ID!, required): The unique identifier for the specific inventory level

## Returned Object: InventoryLevel
The query returns an object with the following key fields:
- `id`: Unique identifier for the inventory level
- `quantities`: Detailed inventory quantity breakdowns
- `item`: Associated inventory item details
- `location`: Location information for the inventory

### Quantity Types
Supported quantity names include:
- `available`
- `incoming`
- `committed`
- `damaged`
- `on_hand`
- `quality_control`
- `reserved`
- `safety_stock`

## Example Query
```graphql
query {
  inventoryLevel(id: "gid://shopify/InventoryLevel/523463154?inventory_item_id=30322695") {
    id
    quantities(names: ["available", "incoming", "committed"]) {
      name
      quantity
    }
    item {
      id
      sku
    }
    location {
      id
      name
    }
  }
}
```

## Available Fields
- `id`: Unique identifier for the inventory level
- `quantities`: Array of quantity objects with name and quantity
- `item`: InventoryItem object with details like SKU
- `location`: Location object with location details
- `canDeactivate`: Whether the inventory level can be deactivated
- `createdAt`: Timestamp when the inventory level was created
- `updatedAt`: Timestamp when the inventory level was last updated

## Supported Languages/Platforms
- GraphQL
- React Router
- Node.js
- Ruby
- cURL

## API Details
- API Version: 2025-10
- Type: GraphQL Admin Query

## Key Use Cases
- Retrieve detailed inventory levels for a specific item
- Check inventory quantities across different states
- Get location and item details for inventory management
- Monitor inventory across multiple locations
- Track different inventory states (available, committed, incoming, etc.)

## Best Practices
- Use the full global ID including inventory_item_id parameter
- Select only the quantity types you need
- Utilize the query for location-specific inventory management
- Monitor different quantity states for comprehensive inventory tracking
