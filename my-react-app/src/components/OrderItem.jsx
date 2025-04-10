import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getImgUrl } from './utils';

const OrderItem = ({ productid , productitem}) => { 
  const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const accessToken = localStorage.getItem("accessToken");
  useEffect(() => {

    const fetchOrder = async () => {
        try {
            const response = await axios.get(`${API_GATEWAY_BASE_URL}/products/${productid}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "product/json",
            },
        });
            setProduct(response.data);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    fetchOrder();
}, [productid]);

if (loading) {
  return <div className="loading-text">Loading...</div>;
}

if (error) {
  return <div>Error: {error}</div>;
}

if (!product) {
  return <div>No order found</div>;
}

return (
    <div className="product-item">
      <img src={getImgUrl(product.image)} alt={product.product_name} height={"200px"} />
      <p>{product.product_name}</p>
      <br></br>
      <p>Product price: ${product.price}</p>
      <p>Quantity ordered: {productitem.quantity}</p>
      <p>Quantity price: ${product.price * productitem.quantity}</p>
    </div>
  );
};

export default OrderItem;