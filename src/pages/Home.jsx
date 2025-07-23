import React from 'react';
import { FaPhone, FaWhatsapp, FaInstagram, FaMapMarkerAlt } from 'react-icons/fa';

const ContactPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-0 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto m-0 pt-0">
        {/* Başlık */}
        <div className="text-center m-0 p-0">
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          {/* İletişim Bilgileri */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">İletişim Bilgileri</h2>
            <div className="space-y-6">
              <div className="flex items-start">
                <div className="flex-shrink-0 bg-purple-100 p-3 rounded-lg">
                  <FaPhone className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Telefon</h3>
                  <p className="mt-1 text-gray-500">+90 (212) 123 45 67</p>
                  <p className="mt-1 text-gray-500">+90 (555) 123 45 67</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 bg-purple-100 p-3 rounded-lg">
                  <FaMapMarkerAlt className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">Adres</h3>
                  <p className="mt-1 text-gray-500">
                    Teknoloji Geliştirme Bölgesi<br />
                    No: 123, Kat: 5<br />
                    Şişli/İstanbul, Türkiye
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-12">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Çalışma Saatleri</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <ul className="space-y-2">
                  <li className="flex justify-between">
                    <span className="text-gray-500">Pazartesi - Cuma</span>
                    <span className="font-medium text-gray-900">09:00 - 18:00</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-gray-500">Cumartesi</span>
                    <span className="font-medium text-gray-900">10:00 - 16:00</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-gray-500">Pazar</span>
                    <span className="font-medium text-gray-900">Kapalı</span>
                  </li>
                </ul>
              </div>
            </div>

            <div className="mt-12">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Sosyal Medya</h3>
              <div className="flex space-x-4">
                {/* WhatsApp */}
                <a
                  href="https://wa.me/905345841825"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-green-500 text-white p-3 rounded-full hover:bg-green-600 transition-colors"
                >
                  <FaWhatsapp className="h-5 w-5" />
                </a>
                {/* Instagram */}
                <a
                  href="https://www.instagram.com/meseriletisim?igsh=MXhrZDI3OWhxOXY1aQ=="
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-3 rounded-full hover:from-purple-600 hover:to-pink-600 transition-colors"
                >
                  <FaInstagram className="h-5 w-5" />
                </a>
              </div>
            </div>
          </div>

          {/* Konum Haritası */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <h2 className="text-2xl font-bold text-gray-900 p-8 pb-4">Konumumuz</h2>
            {/* Google Harita Embed Kodu */}
            <div className="h-96 w-full">
              <iframe
                title="Meser İletişim Ofisi"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d195.5781048837568!2d38.323118367459095!3d38.34320280000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x407637abfad6c157%3A0x1932f803238247ce!2zSG_Fn2hhbmzEsSBLdWFmw7ZyIFNhbG9udQ!5e0!3m2!1sen!2str!4v1753293887740!5m2!1sen!2str"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                allowFullScreen=""
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;