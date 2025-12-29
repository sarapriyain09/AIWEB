export type User = {
  id: number;
  email: string;
};

export type CreditsBalance = {
  plan: "student" | "pro";
  monthly_allowance: number;
  remaining: number;
  resets_at_iso: string;
};

export type CreditUsageItem = {
  id: string;
  at_iso: string;
  action: string;
  cost: number;
};

export type Task = {
  id: number;
  owner_id: number;
  title: string;
  description: string | null;
  is_done: boolean;
};
