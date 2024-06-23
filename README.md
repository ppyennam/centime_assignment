Centime_assignment includes 8 test cases which include:
1.test_registration
2.test_login
3.test_adding_products_to_cart_by_product_type
4.test_adding_products_to_cart_by_search_product_and_quantity
5.test_decreasing_product_quantity_from_cart
6.test_removing_products_from_cart
7.test_updating_address_to_profile
8.test_validating_address_from_profile

The above test cases cover scenarios such as:

Registration:

Register with new credentials
Register with an existing account
Register with a weak password
Successful registration

Login:

Login with valid credentials
Login without a password
Login with an incorrect password
Successful login

Adding Products:

Adding products by product type
Assert error if the product type is not found
Adding products by searching for the product and adding it to the cart in a given quantity
Assert error if the product is not found

Deleting Products:

Removing a complete product from the cart
Assert error if the product to be removed is not found in the cart
Decreasing product quantity by a given size
Assert error if the given size is greater than the product size in the cart
Assert error if the product to decrease is not found in the cart

Updating Address:

Updating the billing address in the profile
Assert error if any of the mandatory fields are not provided in the address
Validating the address by fetching it from the webpage

Used and Followed: python, selenium, selenium webdriver, Pytest Fixtures, Data-Driven Approach, Generated reports.
