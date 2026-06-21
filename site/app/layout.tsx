import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cleo — AI Receptionist for Home Service Businesses",
  description:
    "Cleo answers every call 24/7, books appointments, and syncs data to your CRM. Built for HVAC, plumbing, and electrical companies.",
  openGraph: {
    title: "Cleo — AI Receptionist for Home Service Businesses",
    description:
      "Stop losing jobs to voicemail. Cleo answers every call 24/7, books appointments on your calendar, and syncs data to Jobber, HubSpot, or Housecall Pro.",
    siteName: "CleoVoice",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
