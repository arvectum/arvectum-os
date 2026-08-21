import { DiscountParserSurface } from "./DiscountParserSurface";
import { TenderOperatorSurface } from "./TenderOperatorSurface";
import type { ProductSurfaceContribution } from "./types";

export const productSurfaceRegistry: Readonly<Record<string, ProductSurfaceContribution>> = Object.freeze({
  "tender-operator": {
    id: "tender-operator",
    render: (surface) => <TenderOperatorSurface surface={surface} />,
  },
  "discount-parser": {
    id: "discount-parser",
    render: (surface) => <DiscountParserSurface surface={surface} />,
  },
});
