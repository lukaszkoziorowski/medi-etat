import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Medietat - Oferty pracy dla personelu medycznego",
  description: "Znajdź pracę w placówkach medycznych w Polsce",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl">
      <body>{children}</body>
    </html>
  );
}
