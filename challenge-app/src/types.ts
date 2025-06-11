export interface LoginResponse {
  token: string;
}

// src/types.ts
export interface OrderStatus {
  id: string;
  name: string;
  code: number;
  is_active: boolean;
}

export interface Order {
  id: string;
  title: string;
  description: string;
  code: number;
  is_active: boolean;
  status: OrderStatus;
}

