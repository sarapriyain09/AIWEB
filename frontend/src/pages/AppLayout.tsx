import { Link, Outlet, useLocation } from "react-router-dom";
import React, { useMemo } from "react";

import { Button } from "../components/ui/button";
import { useAuth } from "../state/auth";

export default function AppLayout() {
  const { logout, user } = useAuth();
  const location = useLocation();

  const headerEmail = useMemo(() => user?.email ?? "", [user?.email]);

  const active = useMemo(() => {
    if (location.pathname.startsWith("/app/tasks")) return "tasks";
    return "credits";
  }, [location.pathname]);

  const linkBase = "text-sm font-medium";
  const linkActive = "text-gray-900 underline";
  const linkInactive = "text-gray-600 hover:text-gray-900";

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-5xl px-6 py-4 flex items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <div>
              <div className="text-sm text-gray-500">Signed in</div>
              <div className="text-sm font-medium text-gray-900">{headerEmail}</div>
            </div>

            <nav className="flex items-center gap-4">
              <Link
                to="/app"
                className={[linkBase, active === "credits" ? linkActive : linkInactive].join(" ")}
              >
                Credits
              </Link>
              <Link
                to="/app/tasks"
                className={[linkBase, active === "tasks" ? linkActive : linkInactive].join(" ")}
              >
                Tasks
              </Link>
            </nav>
          </div>

          <Button variant="secondary" onClick={logout}>
            Sign out
          </Button>
        </div>
      </header>

      <main className="mx-auto max-w-5xl p-6">
        <Outlet />
      </main>
    </div>
  );
}
