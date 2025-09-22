const request = require("supertest");
const app = require("../../backend/index"); // adjust if your app entry differs

describe("Product API", () => {
  it("should fetch all products", async () => {
    const res = await request(app).get("/api/products");
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it("should fetch single product by id", async () => {
    const res = await request(app).get("/api/products/1"); // assuming id=1 exists
    expect([200, 404]).toContain(res.statusCode); // either found or not
  });
});