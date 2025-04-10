import React, {useEffect, useState} from "react";
import {Link} from 'react-router-dom'
import axios from "axios";

const formatDate = (dateString) => dateString.split('T')[0];
const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const accessToken = localStorage.getItem("accessToken");

  useEffect(() => {
    if (!loading) return;

    axios.get(`${API_GATEWAY_BASE_URL}/orders`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
    })
    .then((response) => {
        //API response has a "orders" property containing the array, you'll need to extract it correctly.
        const ordersData = response.data.orders || []; // Extract the orders array
        setOrders(ordersData);
        setLoading(false);
    })
    .catch((err) => {
        console.log(err);
        setLoading(false);
    });
}, [loading]);

if (loading) {
  return <div className="loading-text">Loading...</div>;
}

if (!orders) {
  return <div>No order found</div>;
}

return (
    <div className="table-container">
    <h3>Orders</h3>
    
    {/* table that loops through all the orders. Each order has properties: customer_name, email, phone, etc */}
    <table>
        <thead>
            <tr>
                <th>Customer Name</th>
                <th>Number of Products</th>
                <th>Order Submitted on</th>
                <th>View order details</th>
            </tr>
        </thead>
        <tbody>
        {loading ? (
          <tr>
            <td colSpan="4" className="loading-text">Loading orders...</td>
          </tr>
        ) : orders.length === 0 ? (
          <tr>
            <td colSpan="4">No orders to show</td>
          </tr>
        ) : (
          orders.map((order) => (
            <tr key={order.id}>
              <td>{order.customer_name}</td>
              <td>{order.ordered_items.length}</td>
              <td>{formatDate(order.order_time)}</td>
              <td><Link to={`/orders/${order.id}`}>View Details</Link></td>
            </tr>
          ))
        )}
        </tbody>
    </table>
  </div>
);

};

export default Orders;