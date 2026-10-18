import { request } from "./http";

export interface Product {
  id: number | string;
  name: string;
  description?: string;
  price: number;
}
export interface ProductPage {
  items: Product[];
  total?: number;
}

export async function listProducts(p: { search: string; page: number; size: number }): Promise<ProductPage> {
  const q = new URLSearchParams({ page: String(p.page), size: String(p.size) });
  if (p.search) q.set("search", p.search);
  const data = await request<Product[] | ProductPage>(`/products?${q}`);
  return Array.isArray(data) ? { items: data } : data;
}
