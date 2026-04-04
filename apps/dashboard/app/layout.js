import "./globals.css";

export const metadata = {
  title: "ISEYAA — Government Command Center",
  description: "Official oversight and analytics for Ogun State Tourism.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
