# 
mutation {
  orderUpdate(id: "gid://shopify/Order/9876543210", input: {
    email: "updated.email@example.com",
    note: "Updated note: customer requested expedited shipping",
    tags: ["wholesale","priority"],
    shippingAddress: {
      firstName: "John",
      lastName: "Smith",
      address1: "456 New St",
      city: "New City",
      province: "NY",
      country: "US",
      zip: "10001"
    }
  }) {
    order {
      id
      name
      email
      note
      tags
      shippingAddress {
        firstName
        lastName
        address1
        city
        province
        country
        zip
      }
    }
    userErrors {
      field
      message
    }
  }
}