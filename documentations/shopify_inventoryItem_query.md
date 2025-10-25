# inventoryItem GraphQL Query

## Overview
The `inventoryItem` query returns an [InventoryItem](https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem) object by its unique ID. This query allows developers to retrieve detailed information about a specific inventory item in a Shopify store.

## Query Arguments
- `id` (ID!, required): The unique global identifier for the specific inventory item to retrieve

## Possible Returns
An `InventoryItem` object representing goods available for shipping, including:
- Tracking status
- SKU (Stock Keeping Unit)
- Inventory levels
- Associated product variant information

## Key Features
- Retrieve inventory item details
- Check tracking status
- Get inventory levels across locations
- Link inventory items to specific product variants

## Example Queries

### Basic Inventory Item Details
```graphql
query inventoryItem {
  inventoryItem(id: "gid://shopify/InventoryItem/30322695") {
    id
    tracked
    sku
  }
}
```

### Detailed Inventory Information
```graphql
query inventoryItemToProductVariant {
  inventoryItem(id: "gid://shopify/InventoryItem/30322695") {
    inventoryLevels(first: 1) {
      edges {
        node {
          location {
            name
          }
          quantities(names: ["available", "committed"]) {
            name
            quantity
          }
        }
      }
    }
  }
}
```

## Available Fields
- `id`: Unique identifier for the inventory item
- `tracked`: Whether inventory tracking is enabled
- `sku`: Stock Keeping Unit identifier
- `inventoryLevels`: Inventory quantities across different locations
- `variant`: Associated product variant
- `requiresShipping`: Whether the item requires shipping
- `countryCodeOfOrigin`: Country where the item originates
- `harmonizedSystemCode`: International trade classification code

## Supported Languages/Platforms
- GraphQL
- cURL
- React Router
- Ruby
- Node.js

## API Details
- API Version: 2025-10
- Type: GraphQL Admin Query

## Best Practices
- Always use the full global ID when querying inventory items
- Check inventory tracking status before performing inventory operations
- Utilize inventory level quantities for accurate stock management
- Link inventory items to product variants for comprehensive product management

## Common Use Cases
1. Retrieve inventory item details for stock management
2. Check inventory tracking status
3. Get inventory levels across multiple locations
4. Link inventory to specific product variants
5. Retrieve SKU and shipping information
