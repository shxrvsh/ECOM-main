import { render, screen } from "@testing-library/react";
import ProductCard from "../../frontend/src/components/ProductCard"; // adjust path

test("renders product details", () => {
  const fakeProduct = { id: 1, name: "Test Phone", price: 499 };
  render(<ProductCard product={fakeProduct} />);

  expect(screen.getByText(/Test Phone/i)).toBeInTheDocument();
  expect(screen.getByText(/\$499/i)).toBeInTheDocument();
});