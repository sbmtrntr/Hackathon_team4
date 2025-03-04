'use client';

import { Providers } from './providers';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import { Inter } from 'next/font/google';
import type { Metadata } from 'next';
import Header from '@/components/header';

const inter = Inter({ subsets: ['latin'] });

// Chakra UI theme customization
const theme = extendTheme({
  fonts: {
    heading: inter.style.fontFamily,
    body: inter.style.fontFamily,
  },
  colors: {
    brand: {
      50: '#e6ecf5',
      100: '#ccd9eb',
      200: '#b3c6e0',
      300: '#99b3d6',
      400: '#80a0cc',
      500: '#6785c1', // メインカラー
      600: '#526aa9',
      700: '#3d5091',
      800: '#293579',
      900: '#141a60',
    },
  },
  styles: {
    global: {
      body: {
        bg: 'white',
      }
    }
  },
  components: {
    Button: {
      defaultProps: {
        colorScheme: 'brand',
      },
    },
  },
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <head>
        <title>NICOLINK - 2025年卒社会人のためのマッチングアプリ</title>
        <meta name="description" content="2025年卒の同期社会人とつながり、新しい友人や仲間を見つけましょう。" />
      </head>
      <body className={inter.className}>
        <ChakraProvider theme={theme}>
          <Header />
          {children}
        </ChakraProvider>
      </body>
    </html>
  );
}
