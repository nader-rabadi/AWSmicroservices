import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import OrderItem from './OrderItem';

const formatDate = (dateString) => dateString.split('T')[0];

const OrderDetail = () => {
    const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;
    const { id } = useParams(); // Extracting the "id" from the URL
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    
    const accessToken = localStorage.getItem("accessToken");
    useEffect(() => {

        const fetchOrder = async () => {
            try {
                const response = await axios.get(`${API_GATEWAY_BASE_URL}/orders/${id}`, {
                headers: {
                  Authorization: `Bearer ${accessToken}`,
                  "Content-Type": "application/json",
                },
            });
 	            setOrder(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchOrder();
    }, [id]);

    if (loading) {
        return <div className="loading-text">Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!order) {
        return <div>No order found</div>;
    }

    return (
        <div>                       
            <p>
                <button
                    style={{
                        padding: "10px",
                        backgroundColor: "blue",
                        color: "white",
                        fontSize: "1.5rem"
                    }}
                    onClick={() => navigate(-1)}>
                    Back
                </button>
            </p>
            <table className='customer-table'>
                <thead>
                    <tr>
                        <th>Customer Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Ordered on</th>
                        <th>Total Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{order.customer_name}</td>
                        <td>{order.email}</td>
                        <td>{order.phone}</td>
                        <td>{formatDate(order.order_time)}</td>
                        <td>{order.total_amount}</td>
                    </tr>
                </tbody>
            </table>   
            <p><br></br></p>         
            <div className='products-grid'>
                {
                    order.ordered_items.map(item => {
                        return (
                            <div key={item.product_id} >                                
                                <OrderItem productid={item.product_id} productitem={item}/>                                
                            </div>
                        )
                    })
                }
            </div>
        </div>
    );
};

export default OrderDetail;