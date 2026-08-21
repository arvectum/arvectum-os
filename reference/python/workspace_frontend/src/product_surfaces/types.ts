import type { ProductSurfaceContext } from "../types";

export type ProductSurfaceContribution = {
  id: string;
  render: (surface: ProductSurfaceContext) => JSX.Element;
};
