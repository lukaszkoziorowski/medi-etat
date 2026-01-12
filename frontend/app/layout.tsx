import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

// Note: Google Sans is not publicly available via Google Fonts API.
// Using Inter as a similar modern sans-serif alternative that closely matches Google Sans style.
// If you have access to Google Sans font files, we can switch to a local font implementation.
const googleSans = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-google-sans",
  display: "swap",
});

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
    <html lang="pl" className={googleSans.variable}>
      <body>{children}</body>
    </html>
  );
}
