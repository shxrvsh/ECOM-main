import { render, screen, fireEvent } from "@testing-library/react";
import CartButton from "../../frontend/src/components/CartButton"; // adjust path

test("adds item to cart when clicked", () => {
  const onAdd = jest.fn();
  render(<CartButton onAdd={onAdd} />);

  const button = screen.getByRole("button", { name: /add to cart/i });
  fireEvent.click(button);

  expect(onAdd).toHaveBeenCalledTimes(1);
});