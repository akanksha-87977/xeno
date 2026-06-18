import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {

  title: "Global Transaction Validator",
  description: "Customer intelligence and transaction validation platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

