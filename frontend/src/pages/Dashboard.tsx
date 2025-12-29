import React, { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { useAuth } from "../state/auth";
import * as api from "../services/api";
import type { CreditsBalance, CreditUsageItem } from "../services/types";

function fmtIso(iso: string): string {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export default function DashboardPage() {
  const { token } = useAuth();

  const [balance, setBalance] = useState<CreditsBalance | null>(null);
  const [usage, setUsage] = useState<CreditUsageItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (!token) return;
      setLoading(true);
      setError(null);
      try {
        const [b, u] = await Promise.all([api.getCreditsBalance(token), api.getCreditsUsage(token)]);
        if (!cancelled) {
          setBalance(b);
          setUsage(u);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load credits");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, [token]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Credits Dashboard</h1>
        <p className="text-sm text-gray-600">Track your monthly AI credits and usage.</p>
      </div>

        {error ? <div className="text-sm text-red-600">{error}</div> : null}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Balance</CardTitle>
              <CardDescription>Monthly credits remaining</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-sm text-gray-600">Loading...</div>
              ) : balance ? (
                <div className="space-y-2">
                  <div className="text-3xl font-semibold">{balance.remaining}</div>
                  <div className="text-sm text-gray-600">
                    Allowance: {balance.monthly_allowance} / month
                  </div>
                  <div className="text-sm text-gray-600">Resets: {fmtIso(balance.resets_at_iso)}</div>
                </div>
              ) : (
                <div className="text-sm text-gray-600">No data</div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Plan</CardTitle>
              <CardDescription>Current subscription tier</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-sm text-gray-600">Loading...</div>
              ) : balance ? (
                <div className="space-y-2">
                  <div className="text-2xl font-semibold capitalize">{balance.plan}</div>
                  <div className="text-sm text-gray-600">
                    Upgrade and billing will be wired to Stripe (stubbed for now).
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-600">No data</div>
              )}
            </CardContent>
          </Card>
        </div>

      <Card>
        <CardHeader>
          <CardTitle>Usage</CardTitle>
          <CardDescription>Recent credit usage events</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-sm text-gray-600">Loading...</div>
          ) : usage.length ? (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-500">
                    <th className="py-2 pr-4">When</th>
                    <th className="py-2 pr-4">Action</th>
                    <th className="py-2 pr-4">Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {usage.map((u) => (
                    <tr key={u.id} className="border-t">
                      <td className="py-2 pr-4 whitespace-nowrap">{fmtIso(u.at_iso)}</td>
                      <td className="py-2 pr-4">{u.action}</td>
                      <td className="py-2 pr-4">{u.cost}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-sm text-gray-600">No usage yet</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
