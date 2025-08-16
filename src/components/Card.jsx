import React, { useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination, Zoom } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/zoom";

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
  const [isModalOpen, setIsModalOpen] = useState(false);

  const rawImages = Array.isArray(product?.images)
    ? product.images
    : product?.image
    ? [product.image]
    : [];

  const resolved = rawImages.map(resolveAsset).filter(Boolean);

  return (
    <>
      <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition-shadow">
        {/* Görseller - küçük slider */}
        <div className="w-full bg-white">
          {resolved.length ? (
            <Swiper
              modules={[Pagination]}
              pagination={{ clickable: true }}
              spaceBetween={10}
              slidesPerView={1}
              className="h-64 sm:h-80 md:h-96 cursor-pointer"
              onClick={() => setIsModalOpen(true)}
            >
              {resolved.map((src, idx) => (
                <SwiperSlide
                  key={idx}
                  className="flex items-center justify-center"
                >
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

      {/* 🔥 Fullscreen Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center">
          {/* Kapatma Butonu */}
          <button
            onClick={() => setIsModalOpen(false)}
            className="absolute top-4 right-4 text-white text-3xl font-bold z-50"
          >
            ✖
          </button>

          {/* Fullscreen Swiper */}
          <Swiper
            modules={[Navigation, Pagination, Zoom]}
            navigation
            pagination={{ clickable: true }}
            zoom={{ maxRatio: 4 }}
            spaceBetween={10}
            slidesPerView={1}
            className="w-full h-full"
          >
            {resolved.map((src, idx) => (
              <SwiperSlide
                key={idx}
                className="flex items-center justify-center"
              >
                <div className="swiper-zoom-container flex items-center justify-center">
                  <img
                    src={src}
                    alt={`${product.name} ${idx + 1}`}
                    className="object-contain w-full h-full"
                  />
                </div>
              </SwiperSlide>
            ))}
          </Swiper>
        </div>
      )}
    </>
  );
}
