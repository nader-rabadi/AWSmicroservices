import React from 'react';
import { getImgUrl } from './utils';

const ProductItem = ({ product, formInfo, changeHandler }) => {  
  const imgUrl = getImgUrl(product.image)

  return (
    <div className="product-item">
      <img src={imgUrl} alt={product.product_name} height={"200px"} />
      <p>{product.product_name}<br></br>${product.price}</p>
      <p>
        Quantity:{" "}
        <input
          type="number"
          name={product.product_name}
          value={formInfo[product.product_name]?.quantity || 0}
          onChange={changeHandler}
          onWheel={(e) => e.target.blur()} // Prevent wheel scroll on input field
          min="0"
          max={product.inventory_count}
          className="input-style"
        />
      </p>
      <p>Left in stock: {parseInt(product.inventory_count) === 0 ? "Out of stock" : product.inventory_count}</p>
    </div>
  );
};

export default ProductItem;