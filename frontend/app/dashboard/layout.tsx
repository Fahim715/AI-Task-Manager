import { AppProvider } from "../../lib/hooks/useAppState";
import { Navbar } from "../../components/Navbar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AppProvider>
      <Navbar />
      <main className="px-6 py-8">{children}</main>
    </AppProvider>
  );
}
