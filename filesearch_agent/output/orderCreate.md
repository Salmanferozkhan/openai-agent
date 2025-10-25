# 
mutation {
  orderCreate(order: {
    lineItems: [
      {
        variantId: "gid://shopify/ProductVariant/111222333",
        quantity: 2,
        customAttributes: [{key: "gift_note", value: "Happy Birthday!"}]
      }
    ],
    customer: {id: "gid://shopify/Customer/444555666"},
    shippingAddress: {
      firstName: "Jane",
      lastName: "Doe",
      address1: "123 Example St",
      city: "Sample City",
      province: "CA",
      country: "US",
      zip: "90001"
    },
    billingAddress: {
      firstName: "Jane",
      lastName: "Doe",
      address1: "123 Example St",
      city: "Sample City",
      province: "CA",
      country: "US",
      zip: "90001"
    },
    currencyCode: USD,
    email: "jane.doe@example.com",
    transactions: [
      {kind: CAPTURE, gateway: "manual", amount: "39.98"}
    ],
    note: "Imported order from external system"
  }) {
    order {
      id
      name
      email
      totalPrice
      lineItems(first: 10) {
        edges {
          node {
            title
            quantity
            variant {
              id
            }
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