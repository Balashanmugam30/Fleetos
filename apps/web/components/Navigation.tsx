"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Truck, 
  Package, 
  Route as RouteIcon, 
  Activity, 
  Cpu, 
  PhoneCall, 
  Settings as SettingsIcon,
  LayoutDashboard,
  ShieldCheck
} from "lucide-react";

export function Navigation() {
  const pathname = usePathname();

  const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/fleet", label: "Fleet", icon: Truck },
    { href: "/shipments", label: "Shipments", icon: Package },
    { href: "/routes", label: "Routes", icon: RouteIcon },
    { href: "/events", label: "Events", icon: Activity },
    { href: "/optimization", label: "Optimizer", icon: Cpu },
    { href: "/ai", label: "ATLAS AI", icon: PhoneCall },
    { href: "/settings", label: "Settings", icon: SettingsIcon },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo & Brand Title */}
          <div className="flex items-center space-x-3">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-9 h-9 bg-brand-600 rounded-lg flex items-center justify-center text-white font-black text-xl shadow-sm">
                F
              </div>
              <span className="text-xl font-bold tracking-tight text-slate-900">
                FLEET<span className="text-brand-600">OS</span>
              </span>
            </Link>
            <span className="hidden md:inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-brand-50 text-brand-700 border border-brand-200">
              <ShieldCheck className="w-3.3 h-3.3 mr-1 text-brand-600" />
              Control Tower Active
            </span>
          </div>

          {/* Navigation Links */}
          <nav className="flex space-x-1 sm:space-x-2 items-center">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`inline-flex items-center px-3 py-2 text-xs font-semibold rounded-lg transition-colors ${
                    isActive
                      ? "bg-brand-50 text-brand-700 border border-brand-200"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                  }`}
                >
                  <Icon className="w-4 h-4 mr-1.5" />
                  <span className="hidden lg:inline">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}
