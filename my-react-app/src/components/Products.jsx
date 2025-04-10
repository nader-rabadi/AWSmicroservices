import { useEffect, useState } from 'react';
import ProductList from './ProductList';
import { useNavigate } from "react-router-dom";
import axios from 'axios'

const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;

const Products = () => {
  const navigate = useNavigate();
  const [formInfo, setFormInfo] = useState({});

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios
    .get(`${API_GATEWAY_BASE_URL}/products`)
    .then((response) => {
      //API response has a "products" property containing the array, you'll need to extract it correctly.
      const productsData = response.data.products || []; // Extract the products array

      setProducts(productsData);
      setLoading(false);
      })
      .catch((err) => {
        console.log(err); 
        setLoading(false);
      });
    }, []);

    useEffect(() => {
      if (loading) return; // Wait until loading is complete

      if (Array.isArray(products) && products.length > 0) {
        const newInitialQuantities = products.reduce((acc, product) => {
          acc[product.product_name] = {
            id: product.id,
            quantity: 0,
            price: product.price,
            inventory_count: product.inventory_count,
            image: product.image
          };
          return acc;
        }, {});
        setFormInfo(newInitialQuantities);
      }
    }, [products, loading]);
        
    const changeHandler = (e) => {
      const { name, value } = e.target;
      const productInfo = formInfo[name];
  
      // Converts the input value to an integer.
      // Parse the input value and ensure it's a number
      let newValue = parseInt(value, 10);
      // Ensure the value doesn't go below 0 or above inventory_count
      newValue = Math.max(0, Math.min(newValue, productInfo.inventory_count));

      setFormInfo({
        // The "...formInfo" creates a shallow copy of that form.
        // This means all the properties of formInfo are copied
        // into the new object. The spread operator is essentially
        // spreading the existing form properties into the new state object.

        ...formInfo, // Spread the formInfo
        [name]: {    // Update only the [name] property
          ...productInfo, // Spread existing product info
          //quantity: parseInt(value), // Only update the quantity
          quantity: newValue, // I added this one. Update only the quantity property
        },
      });
    };
      
    // Function to compute total price
    const calculateTotal = () => {
      if (Array.isArray(products) && products.length > 0) {
        return products
          .reduce((total, product) => {
            const quantity = formInfo[product.product_name]?.quantity || 0;            
            const price = parseFloat(product.price);
            return total + price * quantity;
          }, 0)
          .toFixed(2); // Use toFixed(2) to format it as a decimal number
      } else {
        return '0.00';
      }
    };
    
    const submitHandler = (e) => {
        e.preventDefault();

        // Filter out products where quantity is 0
        const productsToSubmit = Object.entries(formInfo)
        .filter(([name, { quantity }]) => quantity > 0)
        .map(([name, details]) => ({ name, ...details }));

        if (productsToSubmit.length === 0) {
          return;
        }

        navigate("/customerinfoform", { state: { productsToSubmit } })                
    };

    return (
      <div className="products" id="products-link">
        <h2>Products</h2>
        <form onSubmit={submitHandler} id="order_form">          
          <ProductList
            products={products}
            formInfo={formInfo}
            changeHandler={changeHandler}
          />         
          <input type="submit" value="Checkout" />
        </form>
        <h3>Total Price: ${calculateTotal()}</h3>
      </div>
    );
  };
  
  export default Products;