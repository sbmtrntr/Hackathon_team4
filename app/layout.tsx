import { Providers } from './providers';
import type { Metadata } from 'next';
import Header from '@/components/header';

export const metadata: Metadata = {
  title: 'Connect - Find Your Perfect Match',
  description: 'A modern matching platform for meaningful connections',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <Header />
          {children}
          </Providers>
      </body>
    </html>
  );
}
