import "./globals.css";

export const metadata = {
  title: "ISEYAA — Host Dashboard",
  description: "Manage your listings, orders, and business on ISEYAA.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
