/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  images: {
    unoptimized: true,
  },
  i18n: {
    locales: ['en', 'ar'],
    defaultLocale: 'en',
    localeDetection: true,
  },
}

module.exports = nextConfig
