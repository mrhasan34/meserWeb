import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

// src/assets klasöründeki tüm görselleri topla
const imagesCtx = require.context("../assets", false, /\.(png|jpe?g|svg)$/);

function resolveAsset(path) {
  if (!path) return null;
  const fileName = path.split("/").pop();
  try {
    const mod = imagesCtx(`./${fileName}`);
    return mod?.default || mod;
  } catch {
    return null;
  }
}

export default function Card({ product }) {
  // destek: product.images (array) veya legacy product.image (string)
  const rawImages = Array.isArray(product?.images)
    ? product.images
    : product?.image
    ? [product.image]
    : [];

  const resolved = rawImages.map(resolveAsset).filter(Boolean);

  return (
    <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition-shadow">
      {/* Görseller - tam genişlik slider */}
      <div className="w-full bg-black">
        {resolved.length ? (
          <Swiper
            modules={[Navigation, Pagination]}
            navigation
            pagination={{ clickable: true }}
            spaceBetween={10}
            slidesPerView={1}
            className="h-64 sm:h-80 md:h-96"
          >
            {resolved.map((src, idx) => (
              <SwiperSlide key={idx} className="flex items-center justify-center">
                <img
                  src={src}
                  alt={`${product.name} ${idx + 1}`}
                  className="object-contain w-full h-full"
                />
              </SwiperSlide>
            ))}
          </Swiper>
        ) : (
          <div className="text-red-500 flex items-center justify-center h-64">
            Görsel yok
          </div>
        )}
      </div>

      {/* Ürün detayları */}
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-2">{product.name}</h2>
        <p className="text-gray-600 mb-4">{product.description}</p>
      </div>
    </div>
  );
}
