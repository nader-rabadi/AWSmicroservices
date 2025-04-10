import React from 'react';
import ProductItem from './ProductItem';

const ProductList = ({ products, formInfo, changeHandler }) => {
  if (!Array.isArray(products) || products.length === 0) {
    return <p className="loading-text">Loading...</p>;
  }

  return (
    <div className="products-grid">
      {products.map((product, idx) => (
        <ProductItem
          key={idx}
          product={product}
          formInfo={formInfo}
          changeHandler={changeHandler}
        />
      ))}
    </div>
  );
};

export default ProductList;