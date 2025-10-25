# 
mutation {
  productCreate(product: {
    title: "Sample T-Shirt",
    descriptionHtml: "<strong>Comfortable cotton t‑shirt</strong>",
    vendor: "Example Brand",
    productType: "Apparel",
    tags: ["summer", "cotton", "t-shirt"],
    options: [
      {name: "Size", values: ["S","M","L","XL"]},
      {name: "Color", values: ["Red","Blue"]}
    ],
    variants: [
      {title: "Red / M", sku: "TSHIRT-RED-M", price: "19.99", inventoryPolicy: CONTINUE}
    ],
    status: ACTIVE
  }) {
    product {
      id
      title
      handle
      options {
        name
        values
      }
      variants(first: 10) {
        edges {
          node {
            id
            sku
            price
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}