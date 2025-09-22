import { render, screen } from "@testing-library/react";
import App from "../../frontend/src/App";

test("renders homepage", () => {
  render(<App />);
  const heading = screen.getByText(/welcome/i); // Adjust if your App.js text differs
  expect(heading).toBeInTheDocument();
});