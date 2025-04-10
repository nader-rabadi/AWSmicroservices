
export const getImgUrl = (fileName) => {
    const S3_BUCKET_URL = import.meta.env.VITE_PRODUCTS_IMAGES_BUCKET_URL
    const imgUrl = `${S3_BUCKET_URL}/${fileName}`
  
    return imgUrl;
  }
